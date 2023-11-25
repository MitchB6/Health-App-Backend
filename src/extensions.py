from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate


db=SQLAlchemy()
api=Api(doc='/docs')
migrate = Migrate()