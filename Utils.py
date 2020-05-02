import csv
import DBManager

def getMessages():
    filename = 'chatdata\movie_lines.txt'
    csvDelimiter = '#'
    messages = []
    with open(filename, 'r') as file:
        messages = csv.DictReader(file, delimiter=csvDelimiter)
        return list(messages)

def addUserToDB():
    messages = getMessages()
    list_usernames = list(map(lambda m: (m['user_code'], m['username']), messages))
    list_unique_usernames = list(set(list_usernames))

    dbm = DBManager.DBManager('localhost', '27017', 'chatdb')

    usermap = {}
    for e in list_unique_usernames:
        res = dbm.create_user(e[1])
        usermap[e[0]] = str(res)

    list_chats = list(map(lambda m: m['chat_code'], messages))
    list_unique_chats = list(set(list_chats))

    chatmap = {}
    for e in list_unique_chats:
        chat_messages = filter(lambda m: m['chat_code'] == e, messages)
        list_users_code = list(map(lambda m: m['user_code'], chat_messages))
        list_unique_users_code = list(set(list_users_code))
        list_unique_users_id = list(map(lambda c: usermap[c], list_unique_users_code))
        res = dbm.create_chat(list_unique_users_id)
        chatmap[e] = str(res)

    for m in messages:
        message = {'user_id': usermap[m['user_code']], 'text': m['text']}
        dbm.chat_add_message(chatmap[m['chat_code']], message)