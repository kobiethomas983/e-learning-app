from flask import jsonify
from flask_restx import Resource
from sqlalchemy.exc import SQLAlchemyError

from api.models.api_models import categories_namespace
from api.models.models import Category

categories_api = categories_namespace


@categories_api.route("")
class Categories(Resource):
    def get(self):
        try:
            categories = Category.query.all()
            return jsonify([cat.to_dict() for cat in categories])
        except SQLAlchemyError as error:
            print(f"Database error: {error}")
        except Exception as error:
            print(f"Internal error: {error}")
    