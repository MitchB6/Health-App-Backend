from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

db = SQLAlchemy()
Base = automap_base()

def init_app(app):
    db.init_app(app)

    with app.app_context():
        Base.prepare(db.engine, reflect=True)