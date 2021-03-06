from blacklist import BLACKLIST
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended.utils import get_jwt, get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                        type = str,
                        required = True,
                        help = "This field cannot be blank."
                )
_user_parser.add_argument('password',
                        type = str,
                        required = True,
                        help = "This field cannot be blank."
                    )


class UserRegister(Resource):
    
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201

      
class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        return user.json()

    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        user.delete_from_db()
        return {'message': 'User deleted'}, 200

      
class UserLogin(Resource):

    @classmethod
    def post(cls):
        # get data from _user_parser
        data = _user_parser.parse_args()
        
        # find user in database
        user = UserModel.find_by_username(data['username'])
        
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity = user.id, fresh = True)
            refresh_token = create_refresh_token(identity = user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti'] # jti is a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200


class TokenRefresh(Resource):
    # if a user just logged in then he has fresh token
    # if token is not Fresh it means they didn't just log in
    # refresh token purpose is to ask for a new access token 
    @jwt_required(refresh = True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity = current_user, fresh = False)
        return {'access_token': new_token}, 200

