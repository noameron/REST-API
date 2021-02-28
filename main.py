import secrets
import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from blacklist import BLACKLIST
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import (TokenRefresh, User, UserLogin, UserLogout,
                            UserRegister)

app = Flask(__name__)
# DATABASE_URL is a Postgres variable defined at Heroku server
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = secrets.token_urlsafe(16)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app) 

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    # first user to be created is Admin
    # Instaed of hard-coding, this should be read from config file or database 
    if identity == 1: 
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(_decrypted_header, decrypted_body):
    return decrypted_body['jti'] in BLACKLIST

# fresh token expires after 15 min
@jwt.expired_token_loader
def expired_token_callback(_decrypted_header, _decrypted_body):
    return {
        'description': 'The token has expired',
        'error': 'token_expired',
        }, 401

# will be prompt when user send bad token back
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'description': 'Signature verification failed.',
        'error': 'invalid_token',
        }, 401

# will be prompt when user don't send jwt back at all
@jwt.unauthorized_loader
def missing_token_callback(error):
    return {
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required',
        }, 401

# will be prompt when user don't send fresh jwt when it is required
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return {
        'description': 'The token is not fresh',
        'error': 'fresh_token_required',
    }, 401

# will be prompt when user don't send jwt back at all
@jwt.revoked_token_loader
def revoked_token_callback(_decrypted_header, decrypted_body):
    return {
        'description': 'The token has been revoked',
        'error': 'token_revoked',
    }, 401


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
