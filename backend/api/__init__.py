import os
import json
import psycopg2

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_restx import Api


base_dir = os.path.dirname(os.path.realpath(__file__))
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@localhost:5432/e-learning-db"
    
    db.init_app(app)
    CORS(app)
    
    api = Api(app)
    from .routes.courses import course_api
    api.add_namespace(course_api, path='/courses')

    with app.app_context():
        db.create_all() #checks if tables exists, if dont creates them
    
    return app


