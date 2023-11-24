from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY=config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
   
    SQLALCHEMY_DATABASE_URI = config('MYSQL_DATABASE_URI')
    
class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True
    
class ProdConfig(Config):
    DEBUG = False
    pass

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI='MYSQL_DATABASE_URI'
    SQLALCHEMY_ECHO=False
    TESTING=True
    pass

