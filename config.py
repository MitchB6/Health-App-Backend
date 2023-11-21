from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY=config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    
    #MySQL
    SQLALCHEMY_DATABASE_URI = config('MYSQL_DATABASE_URI')
    
    #SQLite
    SQLALCHEMY_BINDS = {
        'pictures': config('SQLITE_DATABASE_URI', default=f"sqlite:///"+os.path.join(BASE_DIR, 'dev.db'))
    }
    
class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True
    
class ProdConfig(Config):
    DEBUG = False
    pass

class TestConfig(Config):
    TESTING = True
    pass

