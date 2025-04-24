from flask_restx import fields, Namespace

course_namespace = Namespace(name="courses", description="Course API")
categories_namespace =  Namespace(name="categories", description="Categories API")
admin_namespace = Namespace(name="admin", description="Admin API")
auth_namespace = Namespace(name="authentication", description="Authentication API")


course_model = admin_namespace.model(
    'Course',
    {
        "title": fields.String(required=True),
        "author": fields.String(required=True),
        "free": fields.Boolean(required=True),
        "overview": fields.String(),
        "img": fields.String(),
        "url": fields.String(required=True)
    }
)

login_model = auth_namespace.model(
    'Login',
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True)
    }
)