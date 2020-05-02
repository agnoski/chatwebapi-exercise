from flask import Flask
from flask import request
from flask import Response
from flask import jsonify

import DBManager
import NLTKManager

app = Flask(__name__)

dbm = DBManager.DBManager('localhost', '27017', 'chatdb')
nltkm = NLTKManager.NLTKManager()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user/create/<username>')
def create_user(username):
    user_id = dbm.create_user(username)
    return str(user_id)

@app.route('/chat/create')
def create_chat():
    users_id = list(request.args.values())
    chat_id = dbm.create_chat(users_id)
    return str(chat_id)

@app.route('/chat/<chat_id>/adduser')
def chat_add_user(chat_id):
    user_id = request.args.get('user_id')
    dbm.chat_add_user(chat_id, user_id)
    return chat_id

@app.route('/chat/<chat_id>/addmessage')
def chat_add_message(chat_id):
    message = {'user_id': request.args.get('user_id'), 'text': request.args.get('text')}
    message_id = dbm.chat_add_message(chat_id, message)
    return str(message_id)

@app.route('/chat/<chat_id>/list')
def chat_messages_list(chat_id):
    messages_list_json = dbm.chat_messages_list_json(chat_id)
    resp = Response(messages_list_json, status=200, mimetype='application/json')
    return resp

@app.route('/chat/<chat_id>/sentiment')
def chat_sentiment_list(chat_id):
    messages = dbm.chat_messages_list(chat_id)
    sentiments = nltkm.evaluate_messages(messages)
    return jsonify(sentiments)

@app.route('/user/<user_id>/recommend')
def user_recommend(user_id):
    user_messages_list = dbm.user_messages_list(user_id)
    random_users_messages_lists = dbm.random_users_messages_lists(user_id)
    return jsonify([{"len 1": len(user_messages_list)}, {"len 2": len(random_users_messages_lists)}])
    #return jsonify([{"user": "pippo"}, {"user": "pluto"}, {"user": "paperino"}])