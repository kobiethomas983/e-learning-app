from flask import jsonify
from flask_restx import Resource
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash  
from sqlalchemy.exc import SQLAlchemyError


from api.models.api_models import auth_namespace, login_model, create_account_model
from api.models.models import User, User_Roles
from api.utils import ROLES

from api import db

auth_api = auth_namespace

# TODO: Create a signup endpoint
# TODO: Create a access token for a certain amount of time
# TODO: Add more explicit error handling

@auth_api.route("/login")
class Login(Resource):
    @auth_api.expect(login_model)
    def post(self):
        try:
            request_data = auth_api.payload
            email = request_data.get('email')
            password = request_data.get('password')

            user = User.query.filter(User.email == email).one_or_none()
            if not user or check_password_hash(user.password, password):
                auth_api.abort(401, 'invalid credentials')
            
            access_token = create_access_token(identity=email)
            return jsonify({"access_token": access_token})
        except HTTPException as http_error:
            raise http_error
        except Exception as error:
            auth_api.abort(500, f"internal server error: {error}")


@auth_api.route("/create")
class CreateAccount(Resource):
    @auth_api.expect(create_account_model, validated=True)
    def post(self):
        request_data = auth_api.payload
        email = request_data.get("email")

        user = User.query.filter(User.email == email).one_or_none()
        if user:
            auth_api.abort(400, 'resource already exists')

        is_author = False
        if 'is_author' in request_data:
            is_author = request_data['is_author']
        
        try:
            user = User(
                first_name=request_data['first_name'],
                last_name=request_data['last_name'],
                email=request_data['email'],
                password=request_data['password'],
                profile_image=request_data.get('profile_image', ''),
                is_author=is_author
            )
            db.session.add(user)
            db.session.flush() #get user id without full commit

            default_role = User_Roles(
                role_id=ROLES['user'],
                user_id=user.id
            )
            db.session.add(default_role)

            db.session.commit()

            return jsonify(user.to_dict())
        except SQLAlchemyError as error:
            auth_api.abort(500, f"database error: {error}")
        except Exception as error:
            auth_api.abort(500, f"unknown internal error: {error}")

