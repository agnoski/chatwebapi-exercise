from flask import Flask
from flask import request
from flask import Response
from flask import jsonify

from DBManager import DBManager
from NLTKManager import NLTKManager
from ErrorHandler import error_handler

app = Flask(__name__)

dbm = DBManager('localhost', '27017', 'chatdb')
nltkm = NLTKManager()

@app.route('/')
@error_handler
def landing_page():
    return 'Welcome to this awesome chat API!'

@app.route('/user/create/<username>')
@error_handler
def create_user(username):
    user_id = dbm.create_user(username)
    resp = jsonify({'user_id': str(user_id)})
    return resp

@app.route('/chat/create')
@error_handler
def create_chat():
    users_id = list(request.args.values())
    chat_id = dbm.create_chat(users_id)
    resp = jsonify({'chat_id': str(chat_id)})
    return resp

@app.route('/chat/<chat_id>/adduser')
@error_handler
def chat_add_user(chat_id):
    user_id = request.args.get('user_id')
    dbm.chat_add_user(chat_id, user_id)
    resp = jsonify({'chat-id': chat_id})
    return resp

@app.route('/chat/<chat_id>/addmessage')
@error_handler
def chat_add_message(chat_id):
    message = {'user_id': request.args.get('user_id'), 'text': request.args.get('text')}
    message_id = dbm.chat_add_message(chat_id, message)
    resp = jsonify({'message_id': message_id})
    return resp

@app.route('/chat/<chat_id>/list')
@error_handler
def chat_messages_list(chat_id):
    messages_list_json = dbm.chat_messages_list_json(chat_id)
    resp = Response(messages_list_json, status=200, mimetype='application/json')
    return resp

@app.route('/chat/<chat_id>/sentiment')
@error_handler
def chat_sentiment_list(chat_id):
    messages = dbm.chat_messages_list(chat_id)
    sentiments = nltkm.evaluate_messages(messages)
    resp = jsonify(sentiments)
    return resp

@app.route('/user/<user_id>/recommend')
@error_handler
def user_recommend(user_id):
    user_messages_list = dbm.user_messages_list(user_id)
    random_users_messages_lists = dbm.random_users_messages_lists(user_id)
    resp = jsonify([{"len 1": len(user_messages_list)}, {"len 2": len(random_users_messages_lists)}])
    return resp