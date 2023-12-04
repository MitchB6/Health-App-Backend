from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

authoriztions = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the field 'Bearer' [space] and then your token."
    }
}

bcrypt = Bcrypt()
db = SQLAlchemy()
api = Api(title='FITintoTHIS', authorizations=authoriztions,
          security='Bearer Auth', doc='/docs')
migrate = Migrate()
