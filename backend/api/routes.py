from flask import jsonify
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from .models.api_models import api
from .models.models import Course

from . import db

course_api = api

search_parser = reqparse.RequestParser()
search_parser.add_argument('q', type=str, required=True)

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
    

@course_api.route("/search")
class SearchCourse(Resource):
    def get(self):
        query_parameter = search_parser.parse_args().get("q")
        search = f"%{query_parameter}%"

        try:
            courses_by_title = Course.query.filter(Course.title.like(search)).all()
            courses_by_overview = Course.query.filter(Course.overview.like(search)).all()
        except SQLAlchemyError as error:
            course_api.abort(500, f"Server error: {error}")
    
        total_course_collection = courses_by_title + courses_by_overview
        unique_courses = []
        seen = set()

        for crs in total_course_collection:
            if crs not in seen:
                seen.add(crs)
                unique_courses.append(crs)

        return jsonify([c.to_dict() for c in unique_courses])

