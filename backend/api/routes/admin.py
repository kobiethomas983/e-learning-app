from flask import jsonify
from flask_restx import Resource, reqparse

from api.models.api_models import admin_namespace, course_model
from api.models.models import Course

admin_api = admin_namespace


# @admin_api.route("")
# class AdminCourses(Resource):
#     # @admin_api.expect(course_model)
#     # def post(self):
#     #     try:
#     #         request_data = admin_api.payload
#     #         r