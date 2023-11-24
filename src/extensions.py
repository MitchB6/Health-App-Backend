from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db=SQLAlchemy()
api=Api(doc='/docs')
migrate = Migrate()
bcrypt=Bcrypt()