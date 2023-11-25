from flask import Blueprint , render_template, request, flash, redirect, url_for
from .models import Client
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Client.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                flash('Logged in successfuly!', category='success')
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exsit.', category='error')

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
            new_user=Client(email=email, frist_name=fname, password=generate_password_hash(
                password1, "sha256"))
            db.session.add(new_user)
            db.session.commit()     

            flash('account created', category='success')
            return redirect(url_for("auth.signup"))
            #add user

    return render_template("signup/signUp.html")

@auth.route('/home')
def home():
    return render_template("home.html")