# Edit users: Only an admin can update a user or the user themselves
# Delete users: Same thing
#  Get user profile: Not permissions needed just a jwt required
from flask import jsonify
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from api.models.api_models import user_namespace, create_edit_user_model, get_user_model
from api.models.models import User, User_Roles, Role

from api import db

users_api = user_namespace

@users_api.route("/<int:id>")
class UserResource(Resource):
    @jwt_required()
    def get(self, id):
        email_identity = get_jwt_identity()
        user = User.query.filter(User.email == email_identity).one_or_none()
        if not user:
            users_api.abort(401, 'unauthorized')
        
        try:
            profile = User.query.options(joinedload(User.roles))\
                    .filter(User.id == id).one_or_none()
            
            if not profile:
                users_api.abort(404, 'not found')
            
            return jsonify(profile.to_dict(include_roles=True))
        except SQLAlchemyError as error:
            users_api.abort(500, f"internal database error: {error}")
        except Exception as error:
            users_api.abort(500, f"unknown internal error: {error}")

    @jwt_required()
    @users_api.expect(create_edit_user_model, validate=True)
    def put(self, id):
        try:
            email_identity = get_jwt_identity()
            identity = User.query.options(joinedload(User.roles))\
                        .filter(User.id == email_identity)\
                        .one_or_none()
            
            def update_user(existing_user, request_payload):
                existing_user.first_name = request_payload['first_name']
                existing_user.last_name = request_payload['last_name']
                existing_user.email = request_payload['email']
                existing_user.password = request_payload['password']
                existing_user.is_author = request_payload['is_author']
                
                db.session.commit()

                return existing_user

            if not identity:
                users_api.abort(401, 'unauthorized')
            
            updated_user = None
            if identity.id == id:
                updated_user = update_user(identity, users_api.payload)
            elif is_admin(identity):
                user_to_update = User.query.options(joinedload(User.roles))\
                            .filter(User.id == id).one_or_none()
                
                if not user_to_update:
                    users_api.abort(404, 'user not found')
                
                updated_user = update_user(identity, users_api.payload)
            else:
                users_api.abort(401, 'unauthorized to update this profile')
            
            return jsonify(updated_user.to_dict())

        except SQLAlchemyError as error:
            users_api.abort(500, f'internal database error: {error}')
        except Exception as error:
            users_api.abort(500, f'unknown internal error: {error}')
    
    def delete(self, id):
        try:
            email_identity = get_jwt_identity()
            identity = User.query.options(joinedload(User.roles))\
                        .filter(User.id == email_identity)\
                        .one_or_none()
            
            if not identity:
                users_api.abort(401, 'unauthorized')
            
            if identity.id == id:
                identity.delete()
            elif is_admin(identity):
                user_to_delete = User.query.filter(User.id == id).one_or_none()
                if not user_to_delete:
                    users_api.abort(404, 'user not found')
                
                user_to_delete.delete()
            else:
                users_api.abort(401, 'unauthorized to delete this profile')
            
            db.session.commit()
        except SQLAlchemyError as error:
            users_api.abort(500, f'internal database error: {error}')
        except Exception as error:
            users_api.abort(500, f'unknown internal error: {error}')

def is_admin(user):
    return any(role.role_name == 'admin' for role in user.roles)