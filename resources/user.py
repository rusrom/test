from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from models.user import UserModel
from schemas.user import UserSchema


user_schema = UserSchema()


class UserRegister(Resource):
    # Create New User
    def post(self):
        try:
            data_json = request.get_json()
            new_user_object = user_schema.load(data_json)
        except ValidationError as e:
            return e.messages, 400

        # Find such new username in db
        user = UserModel.find_by_username(new_user_object.username)
        if user:
            return {'message': 'such user already exists'}, 400

        # Create new user
        new_user_object.save_to_db()
        return {'user': user_schema.dump(new_user_object)}, 201
