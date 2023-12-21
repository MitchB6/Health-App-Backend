from flask import jsonify, make_response, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import socketio
from flask_socketio import emit
from ..models.chat_model import Chats
from ..extensions import db

chat_ns = Namespace('Chat', description="A namespace for Chat")

chat_history = {}  # Dictionary to store chat history


@chat_ns.route('/')
class Chat(Resource):
  @jwt_required()
  def get(self):
    return jsonify({'message': 'chat check success'})

def get_chats_by_key(chat_key):
    try:
        # Query the database for messages with the specified chat_key
        chats_by_key = Chats.query.filter_by(chatkey=chat_key).all()

        # Convert the records to a list of dictionaries
        chats_list = [
            {
                'chatkey': chat.chatkey,
                'sender': chat.sender,
                'recipient': chat.recipient,
                'message': chat.message,
                'timestamp': chat.timestamp.isoformat()  # Assuming there is a timestamp field
            }
            for chat in chats_by_key
        ]

        return chats_list
    except Exception as e:
        print(f"Error retrieving chats for key {chat_key}: {e}")
        return None

@chat_ns.route('/history/<chat_key>')
class ChatHistory(Resource):
    @jwt_required()
    def get(self, chat_key):
        try:
            # Query the database for messages with the specified chat_key
            messages = Chats.query.filter_by(chatkey=chat_key).all()

            # Convert the messages to a list of dictionaries
            message_list = [
                {
                    'chatkey': message.chatkey,
                    'sender': message.sender,
                    'recipient': message.recipient,
                    'message': message.message,
                }
                for message in messages
            ]

            return jsonify({'chat_history': message_list})
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            return make_response(jsonify({'error': 'Unable to fetch chat history'}), 500)

@socketio.on('send_message')
def handle_send_message(data):
  print(data)
  sender = data['sender']
  recipient = data['recipient']
  text = data['text']

  chat_key = f'{sender}-{recipient}'



  print("this is data",data)
  print("this the key",chat_key)
  print("this the history",chat_history)

  if chat_key not in chat_history:
    chat_history[chat_key] = []
  chat_history[chat_key].append(data)

  emit('new_message', data, room=recipient)
  emit('new_message', data, room=sender)
  new_message = Chats(chatkey=chat_key, sender=sender,
                      recipient=recipient, message=text)

  # Save the new message to the database
  db.session.add(new_message)
  db.session.commit()


@socketio.on('request_history')
def handle_request_history(data):
  print("\n\n\n testing if this works \n request_history \n\n\n")
  user1 = data['user1']
  user2 = data['user2']
  chat_key = f'{user1}-{user2}'
  #chat_key = tuple(sorted([user1, user2]))
  print("chat key",chat_key)
  print("-".join(chat_key))
  chat_historys = get_chats_by_key("user1-user2")
  

  history = chat_history.get(chat_key, [])
  emit('chat_history', chat_historys, room=chat_key)


@socketio.on('connect')
def handle_connect():
  print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
  print('Client disconnected')
