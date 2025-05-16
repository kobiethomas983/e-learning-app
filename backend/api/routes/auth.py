from flask import jsonify
from flask_restx import Resource
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash  


from api.models.api_models import auth_namespace, login_model
from api.models.models import User

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
        
