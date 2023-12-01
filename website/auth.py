from flask import Flask, Blueprint, render_template, request, session, flash, redirect, url_for, jsonify,make_response
from flask_socketio import SocketIO, send, emit
from .models import Client, Chatmessage
from . import db, messages
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)
socketio = SocketIO()

@auth.route('/chatrooms', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        page = request.form.get("submit_button")
        print(page)
        return redirect(url_for("auth.chat"))
    return render_template("chat/baseroom.html")

@auth.route('/chat')
def chat():
    print("json stuff:::", jsonify({'messages': messages}))
    return render_template("chat/chat.html")

# @auth.route('/get_chat_history')
# def get_chat_history():
#     chat_history = ChatMessage.query.all()
#     history_data = [{"username": msg.username, "message": msg.message, "timestamp": msg.timestamp} for msg in chat_history]
#     return jsonify(history_data)

@auth.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data['message']
    
    # You can broadcast the message to all connected clients
    # in a real chat application, you might use Socket.IO for real-time communication
    # Here, we'll just simulate storing the messages in a list
    messages.append(message)
    
    return jsonify({'status': 'Message sent successfully'})

@auth.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify({'messages': messages})


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')
        user = Client.query.filter_by(email=email).first()
        if user:
            hashed_password = user.password # Assuming password is already hashed in the database
            if check_password_hash(hashed_password, password):
                flash('Logged in successfully!', category='success')
                return redirect(url_for("auth.home"))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html")
    
@auth.route('/admin')
def admin():
    return render_template("admin.html")


@auth.route('/logout')
def logout():
    return"<p>Logout<p>"

info = Blueprint('info',__name__)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method =='POST':
        answer = request.form.get('exp')
        if answer == 'No':
            return render_template("signup/info.html")
        else:
            return redirect(url_for("auth.bmi"))
    else:
        return render_template("signup/info.html")
    
@auth.route('/bmi', methods=['GET','POST'])
def bmi():
    if request.method =='POST':
        answer = request.form.get('exp')
        if answer == 'No':
            return render_template("signup/info.html")
        else:
            return redirect(url_for("auth.goal"))
    else:
        return render_template("signup/bmi.html")

@auth.route('/goal', methods=['GET','POST'])
def goal():
    if request.method =='POST':
        answer = request.form.get('exp')
        if answer == 'No':
            return render_template("signup/info.html")
        else:
            return redirect(url_for("views.home"))
    else:
        return render_template("signup/goals.html")

@auth.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.method =='POST':
        email = request.form.get('email')
        check = Client.query.filter_by(email=email).first()
        fname = request.form.get('firstName')
        password1 = request.form.get('pass1')
        password2 = request.form.get('pass2')
        if len(email) < 4:
            flash('email must be greater than 4 characters', category='email')
        elif check:
            flash('This email is already being used', category='error')
        elif len(fname) < 2:
            flash('first name must be greater than 2 characters', category='fname')
        elif len(password1) < 7:
            flash('password must be greater than 7 characters', category='lenpass') 
        elif password2 != password1:
            flash('passwords do not match', category='macpass')
        else:
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
            new_user=Client(email=email, first_name=fname, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()     

            flash('account created', category='success')
            return redirect(url_for("auth.signup"))
            #add user

    return render_template("signup/signUp.html")

@auth.route('/home')
def home():
    return render_template("home.html")