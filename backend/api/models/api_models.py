from flask_restx import fields, Namespace

course_namespace = Namespace(name="courses", description="Course API")
categories_namespace =  Namespace(name="categories", description="Categories API")
admin_namespace = Namespace(name="admin", description="Admin API")
auth_namespace = Namespace(name="authentication", description="Authentication API")
user_namespace = Namespace(name="users", description="User API")

category_model = admin_namespace.model(
    'Category',
    {
        "name": fields.String(required=True)
    }
)


course_model = admin_namespace.model(
    'Course',
    {
        "title": fields.String(required=True),
        "author": fields.String(required=True),
        "free": fields.Boolean(required=True),
        "overview": fields.String(),
        "img": fields.String(),
        "url": fields.String(required=True),
        "categories": fields.List(fields.Nested(category_model), required=True)
    }
)

login_model = auth_namespace.model(
    'Login',
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True)
    }
)


create_edit_user_model = user_namespace.model(
    'User',
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "profile_image": fields.String(),
        "is_author": fields.Boolean(required=True)
    }
)

user_roles_model = user_namespace.model(
    'User Roles',
    {
        'role': fields.String()
    }
)

get_user_model = user_namespace.model(
        'User',
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "profile_image": fields.String(),
        "is_author": fields.Boolean(required=True),
        'roles': fields.List(fields.Nested(user_roles_model))
    }
)