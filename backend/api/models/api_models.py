from flask_restx import Namespace, fields

api = Namespace(name="courses", description="Course API")

course_model = api.model(
    'Course',
    {
        "title": fields.String(),
        "author": fields.String(),
        "free": fields.Boolean(),
        "overview": fields.String(),
        "img": fields.String(),
        "url": fields.String()
    }
)