from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .extensions import db, api, migrate, socketio
from .routes.auth import auth_ns
from .routes.member import member_ns
from .routes.home import home_ns
from .routes.exercise import exercise_ns
from .routes.coach import coach_ns
from .routes.workout import workout_ns
from .routes.admin import admin_ns
from .routes.workout_plan import workoutplan_ns

import os
import pkgutil
import importlib


def import_models():
  # Define the path to the models directory
  models_path = os.path.join(os.path.dirname(__file__), 'models')

  for _, name, _ in pkgutil.iter_modules([models_path]):
    imported_module = importlib.import_module(
        '.' + name, package='src.models')


def create_app(config):
  app = Flask(__name__)
  app.config.from_object(config)
  CORS(app, resources={r"/*": {"origins": "*"}})

  db.init_app(app)

  import_models()
  migrate.init_app(app, db)
  JWTManager(app)

  socketio.init_app(app)

  # Initialize database
  with app.app_context():
    db.create_all()

  @app.route('/')
  def index():
    """fire name don't hate"""
    return jsonify({"message": "FIT THIS"})

  @app.errorhandler(404)
  def not_found(err):
    return jsonify({"message": "I dunno bro its not here"})

  api.init_app(app)
  api.add_namespace(member_ns)
  api.add_namespace(auth_ns)
  api.add_namespace(home_ns)
  api.add_namespace(exercise_ns)
  api.add_namespace(coach_ns)
  api.add_namespace(workout_ns)
  api.add_namespace(admin_ns)
  api.add_namespace(workoutplan_ns)

  @app.shell_context_processor
  def make_shell_context():
    return {
        "db": db
    }

  return app
