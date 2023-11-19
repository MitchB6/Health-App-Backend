from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from .services import authenticate_user
from flask import Flask, send_from_directory

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@main.route('/health')
def health_check():
    try:
        return jsonify({'status': 'UP', 'message': 'Service is healthy'})
    except Exception as e:
        return jsonify({'status': 'DOWN', 'message': 'Service is not healthy'})

@main.route('/login', methods=['POST'])
def login():
    # Get username and password from request
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Authenticate
    user = authenticate_user(username, password)
    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401