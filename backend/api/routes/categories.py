from flask import jsonify
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
import math

from models.api_models import categories_namespace
from models.models import Category

categories_api = categories_namespace


