from flask import jsonify, make_response, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import socketio
from flask_socketio import emit
from ..models.chat_history_model import Chats
from ..extensions import db

chat_ns = Namespace('Chat', description="A namespace for Chat")

chat_history = {}  # Dictionary to store chat history


@chat_ns.route('/')
class Chat(Resource):
  @jwt_required()
  def get(self):
    return jsonify({'message': 'chat check success'})


@socketio.on('send_message')
def handle_send_message(data):
  sender = data['sender']
  recipient = data['recipient']
  text = data['text']
  chat_key = tuple(sorted([sender, recipient]))

  new_message = Chats(chatkey='-'.join(chat_key), message=text)
  db.session.add(new_message)
  db.session.commit()

  if chat_key not in chat_history:
    chat_history[chat_key] = []
  chat_history[chat_key].append(data)

  emit('new_message', data, room=recipient)
  emit('new_message', data, room=sender)


@socketio.on('request_history')
def handle_request_history(data):
  user1 = data['user1']
  user2 = data['user2']
  chat_key = tuple(sorted([user1, user2]))
  print(chat_key)
  print("-".join(chat_key))

  history = chat_history.get(chat_key, [])
  emit('chat_history', history, room=user1)


@socketio.on('connect')
def handle_connect():
  print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
  print('Client disconnected')
