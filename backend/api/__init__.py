import os
import json
import psycopg2

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager

base_dir = os.path.dirname(os.path.realpath(__file__))
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@localhost:5432/e-learning-db"
    app.config['JWT_SECRET_KEY'] = "super-secret-key"
    
    db.init_app(app)
    CORS(app)
    JWTManager(app)
    
    api = Api(app)
    from .routes.courses import course_api
    from .routes.categories import categories_api
    from .routes.admin import admin_api
    from .routes.auth import auth_api
    from .routes.users import users_api

    api.add_namespace(course_api, path='/courses')
    api.add_namespace(categories_api, path='/categories')
    api.add_namespace(admin_api, path="/admin")
    api.add_namespace(auth_api, path="/auth")
    api.add_namespace(users_api, path="/users")

    with app.app_context():
        db.create_all() #checks if tables exists, if dont creates them
    
    return app


