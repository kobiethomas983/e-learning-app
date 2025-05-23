from flask import jsonify
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
import math

from api.models.api_models import course_namespace
from api.models.models import Course, Course_Category_Map

course_api = course_namespace

search_parser = reqparse.RequestParser()
search_parser.add_argument('q', type=str, required=True)

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, default=1)
pagination_parser.add_argument('page_size', type=int, default=10)
pagination_parser.add_argument('author_filter', type=str, default="")

categories_pagination_parser = reqparse.RequestParser()
categories_pagination_parser.add_argument('page', type=int, default=1)
categories_pagination_parser.add_argument('page_size', type=int, default=5)

@course_api.route("")
class Courses(Resource):
    def get(self):
        try: 
            args = pagination_parser.parse_args()
            author_filter = args.get("author_filter")
            page = args.get("page")
            page_size = args.get("page_size")
            offset = (page - 1) * page_size

            query = Course.query
            if author_filter:
               query = query.filter(Course.author == author_filter)

            # joinedload does a eagerly fetch on categories so we don't
            # so we can get all categories for each course all in one sql call
            courses = (
                        query
                        .options(joinedload(Course.categories))
                        .limit(page_size)
                        .offset(offset)
                        .all()
                    )       

            count = query.count()
            total_pages = math.ceil(count / page_size)

            response = {
                'courses': [course.to_dict(include_categories=True, include_author=True) for course in courses],
                'page': page,
                'page_size': page_size,
                'total_course': count,
                'total_pages': total_pages
            }
            return jsonify(response)
        except Exception as error:
            course_api.abort(500, f"error processing request: {error}")
    

@course_api.route("/<id>")
class SingleCourse(Resource):
    def get(self, id):
        course = (
                    Course.query
                    .options(
                        joinedload(Course.categories),
                        joinedload(Course.author)
                    )
                    .filter(Course.id == id)
                    .one_or_none()
        )

        if not course:
            course_api.abort(404, 'course does not exist')
        return jsonify(course.to_dict(include_categories=True, include_author=True))
    
@course_api.route("/categories/<id>")
class CoursesByCategory(Resource):
    def get(self, id):
      try:
        q_params = categories_pagination_parser.parse_args()
        
        courses = Course.query.options(joinedload(Course.categories)) \
                .join(Course_Category_Map, Course.id == Course_Category_Map.course_id) \
                .filter(Course_Category_Map.category_id == id) \
                .paginate(page=q_params.get('page'), per_page=q_params.get('page_size'), error_out=False)

        response_courses = [course.to_dict(include_categories=True, include_author=True) for course in courses]
        response = {
            'courses': response_courses,
            'page': q_params.get('page'),
            'page_size': q_params.get('page_size'),
            'total_course': courses.total,
            'total_page': math.ceil(courses.total/q_params.get('page_size'))
        }
        return jsonify(response)
      except Exception as error:
          course_api.abort(500, f"error processing request: {error}")
      
      

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
