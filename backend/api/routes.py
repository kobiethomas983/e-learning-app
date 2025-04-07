from flask import jsonify
from flask_restx import Resource

from .api_models import api
from .models import Course

from . import db

course_api = api

@course_api.route("")
class Courses(Resource):
    def get(self):
        courses = Course.query.all()
        return jsonify([c.to_dict() for c in courses])
    

@course_api.route("/<id>")
class SingleCourse(Resource):
    def get(self, id):
        course = Course.query.filter(Course.id == id).one_or_none()
        if not course:
            course_api.abort(404, 'course does not exist')
        return jsonify(course.to_dict())


