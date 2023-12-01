from flask import Flask
from .extentions import db
from os import path
from .events import socketio

DB_NAME = "talks.db"
messages = [] 


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hello'
    socketio.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views #chafge back
    from .auth import auth #chafge back

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Client, Chatmessage #chafge back

    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
