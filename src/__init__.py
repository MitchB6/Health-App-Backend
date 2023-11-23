from flask import Flask
from config import DevConfig,ProdConfig,TestConfig
from .extensions import db,api,migrate

#Set config here
Config = DevConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
   
    db.init_app(app)
    migrate.init_app(app,db)
    api.init_app(app)
    
    # Initialize database
    with app.app_context():
        db.create_all()

    # Register blueprints
    from . import routes
    
    return app