from flask import jsonify
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from api.models.api_models import admin_namespace, course_model
from api.models.models import (
    Course, 
    User, 
    User_Roles, 
    Category,
    Course_Category_Map
)
from api import db

admin_api = admin_namespace


roles_to_ids = {
    "admin": 1,
    "user": 2
}

@admin_api.route("")
class AdminCourses(Resource):
    @jwt_required()
    @admin_api.expect(course_model, validate=True)
    def post(self):
    
        email_identity = get_jwt_identity()
        user = User.query.filter(User.email == email_identity).one_or_none()
        user_roles = User_Roles.query.filter(User_Roles.user_id == user.id).all()
        is_admin = list(filter(lambda x: x.role_id == roles_to_ids["admin"], user_roles))

        if not is_admin:
            admin_api.abort(401, "Unauthorized to do this operation")

        request_data = admin_api.payload
        if not request_data.get('categories') or len(request_data.get('categories')) == 0:
            admin_api.abort(400, "categories are required for courses")

        try:
            course = Course(
                title=request_data['title'],
                author=request_data['author'],
                free=request_data['free'],
                overview=request_data['overview'],
                img=request_data['img'],
                url=request_data['url'],
            )
            db.session.add(course)
            
            categories_collection = []
            for cat in request_data['categories']:
                cat_existence = Category.query.filter(Category.name == cat['name']).one_or_none()
                if cat_existence:
                    categories_collection.append(cat_existence.id)
                else:
                   new_category = Category(name=cat['name']) 
                   db.session.add(new_category)
                   db.session.flush() #Get ID without full commit
                   categories_collection.append(new_category.id)

            course_to_categories_map = [Course_Category_Map(course_id=course.id, category_id=cat_id) for cat_id in categories_collection]
            db.session.add_all(course_to_categories_map)

            db.session.commit()
            
            return jsonify(message="course created successfully")
        except SQLAlchemyError as error:
            print(f"Error saving data for course create: {error}")
            admin_api.abort(500, "internal database error")
