from flask_restx import fields, Namespace

course_namespace = Namespace(name="courses", description="Course API")
categories_namespace =  Namespace(name="categories", description="Categories API")

course_model = course_namespace.model(
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