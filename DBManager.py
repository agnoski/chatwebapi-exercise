import pymongo
import random
from bson.objectid import ObjectId
from bson.json_util import dumps

class DBManager:
    def __init__(self, db_host, db_port, db_name):
        self.mongodb_client = pymongo.MongoClient('mongodb://' + db_host + ':' + db_port + '/')
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
        query = {'_id': ObjectId(chat_id)}
        chat = self.db.chats.find_one(query)
        users_id = chat['users_id'].append(user_id)
        new_users_id = {'$set': {'users_id': chat['users_id']}}
        self.db.chats.update_one(query, new_users_id)

    def chat_add_message(self, chat_id, message):
        query = {'_id': ObjectId(chat_id)}
        chat = self.db.chats.find_one(query)

        allowed_users_id = chat['users_id']

        if message['user_id'] in allowed_users_id:
            res = self.db.messages.insert_one(message)
            chat['messages_id'].append(str(res.inserted_id))
            new_messages_id = {'$set': {'messages_id': chat['messages_id']}}
            self.db.chats.update_one(query, new_messages_id)
            return res.inserted_id
        else:
            raise Exception('Access denied')
    
    def chat_messages_list(self, chat_id):
        query = {'_id': ObjectId(chat_id)}
        chat = self.db.chats.find_one(query)

        messages_list = []
        for message_id in chat['messages_id']:
            query_message = {'_id': ObjectId(message_id)}
            message = self.db.messages.find_one(query_message)
            messages_list.append(message)
        
        return messages_list

    def chat_messages_list_json(self, chat_id):
        messages_list = self.chat_messages_list(chat_id)
        return dumps(messages_list)

    def user_messages_list(self, user_id):
        query = {'user_id': user_id}
        messages = self.db.messages.find(query)
        return list(messages)

    def random_users_messages_lists(self, user_id):
        users = self.db.users.find()
        random_users = random.sample(list(users), 2)
        return list(map(lambda u: self.user_messages_list(str(u['_id'])), random_users))