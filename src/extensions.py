from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

authoriztions = {
  'Bearer Auth': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
  }
}

bcrypt=Bcrypt()
db=SQLAlchemy()
api=Api(title='Fit This', authorizations=authoriztions, security='Bearer Auth', doc='/docs')
migrate = Migrate()