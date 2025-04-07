import os
import json
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_restx import Api


base_dir = os.path.dirname(os.path.realpath(__file__))
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base_dir, 'e-learning.db')
    
    db.init_app(app)
    CORS(app)
    
    api = Api(app)
    from .routes import course_api
    api.add_namespace(course_api, path='/courses')
    
    with app.app_context():
        from .models import Course
        db.drop_all() #remove previous data
        db.create_all()

        try:
            with open('course.json', 'r') as file:
                json_courses = json.load(file)
                for jc in json_courses:
                    course = Course(
                        title=jc['title'],
                        author=jc['author'],
                        free=jc['free'],
                        overview=jc['overview'],
                        img=jc['img'],
                        url=jc['url']
                    )
                    db.session.add(course)
                    db.session.commit()
        except SQLAlchemyError as error:
            raise(f"Error: issues saving {error}")
        except FileNotFoundError:
            raise("Error: File not found")
        except json.JSONDecodeError:
            raise("Error: Invalid Json format")
        
    
    return app


