from flask_restx import Resource

from .api_models import api

course_api = api

@course_api.route("")
class Courses(Resource):
    def get(self):
        return {"message": "hello"}