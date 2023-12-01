from .extentions import socketio
from flask_socketio import emit
from flask import jsonify, request
#from . import db (VERY BAD DONT NOT UNCOMMENT VERY VERY BAD)
from .extentions import db
from .models import Chatmessage

users = {}

@socketio.on("connect")
def handle_connect():
    print ('Socket.io Connected successfully')

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined")
    print(request.sid)
    users[username] = request.sid
    print(users)

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None 
    for user in users:
        if users[user] == request.sid:
            username = user
    emit("chat", {"message": message, "username": username}, broadcast=True)

@socketio.on('private_message')
def private_message(username, message):
    recipient_session_id = users[username]
    print("message to user: ",username," message:", message)
    emit("chat", {"message": message, "username": username}, broadcast=True)
    chat_message = Chatmessage(user=username, message=message)
    db.session.add(chat_message)
    db.session.commit()
    print("chat database: ", Chatmessage.query.first())