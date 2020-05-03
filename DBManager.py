import pymongo
import random
from bson.objectid import ObjectId
from bson.json_util import dumps

from ErrorHandler import APIError

class DBManager:
    def __init__(self, db_host, db_port, db_name):
        self.mongodb_client = pymongo.MongoClient(f'mongodb://{db_host}:{db_port}/')
        self.db = self.mongodb_client[db_name]

    def create_user(self, username):
        user = {'username' : username}
        res = self.db.users.insert_one(user)
        return res.inserted_id

    def create_chat(self, users_id):
        chat = {'users_id': users_id, 'messages_id': []}
        res = self.db.chats.insert_one(chat)
        return res.inserted_id

    def chat_add_user(self, chat_id, user_id):
        chat = self.get_chat_from_db(chat_id)
        chat['users_id'].append(user_id)
        new_users_id = {'$set': {'users_id': chat['users_id']}}

        query = {'_id': ObjectId(chat_id)}
        self.db.chats.update_one(query, new_users_id)

    def chat_add_message(self, chat_id, message):
        chat = self.get_chat_from_db(chat_id)
        allowed_users_id = chat['users_id']
        user_id = message['user_id']

        if user_id in allowed_users_id:
            res = self.db.messages.insert_one(message)
            chat['messages_id'].append(str(res.inserted_id))
            new_messages_id = {'$set': {'messages_id': chat['messages_id']}}

            query = {'_id': ObjectId(chat_id)}
            self.db.chats.update_one(query, new_messages_id)
            return res.inserted_id
        else:
            raise APIError(f'Access denied: <user_id> {user_id} can not access <chat_id> {chat_id}')
    
    def chat_messages_list(self, chat_id):
        chat = self.get_chat_from_db(chat_id)
        messages_id = chat['messages_id']
        messages_list = list(map(self.get_message_from_db, messages_id))
        return messages_list

    def chat_messages_list_json(self, chat_id):
        messages_list = self.chat_messages_list(chat_id)
        messages_list_json = dumps(messages_list)
        return messages_list_json

    def user_messages_list(self, user_id):
        query = {'user_id': user_id}
        messages = self.db.messages.find(query)
        messages_list = list(messages)
        return messages_list

    def random_users_messages_lists(self, user_id):
        users = self.db.users.find()
        random_users = random.sample(list(users), 2)
        random_users_messages_id_list = list(map(lambda user: self.user_messages_list(str(user['_id'])), random_users))
        return random_users_messages_id_list

    def get_chat_from_db(self, chat_id):
        query = {'_id': ObjectId(chat_id)}
        chat = self.db.chats.find_one(query)
        if chat is not None:
            return chat
        else:
            raise APIError(f'Invalid <chat_id> {chat_id}')

    def get_message_from_db(self, message_id):
        query_message = {'_id': ObjectId(message_id)}
        message = self.db.messages.find_one(query_message)
        if message is not None:
            return message
        else:
            raise APIError(f'Invalid <message_id> {message_id}')
