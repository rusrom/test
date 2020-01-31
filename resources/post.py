from flask import request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from marshmallow import ValidationError

from schemas.post import PostSchema
from models.post import PostModel

post_schema = PostSchema()
post_list_schema = PostSchema(many=True)


class PostList(Resource):
    def get(self):
        tags = request.args.get('tags')
        if tags:
            # TODO: Need find posts with such tags
            pass
        # return {'posts': [post_schema.dump(post) for post in PostModel.query.all()]}
        return {'posts': post_list_schema.dump(PostModel.query.all())}


class Post(Resource):
    # Get Post by ID
    @jwt_required()
    def get(self, post_id):
        # JWT sugar
        user = current_identity
        print('>>> user_identity >>>', user.id, user.username, user.password)

        post = PostModel.find_post_by_id(post_id)
        if post:
            return post_schema.dump(post)
        return{'message': 'post with such ID not found'}, 404

    # Create New Post
    @jwt_required()
    def post(self):
        # Get info about user.id, user.username, user.password from JWT Token
        user = current_identity
        print('>>> user_identity >>>', user.id, user.username, user.password)

        try:
            data_json = request.get_json()
            data_json['user_id'] = user.id  # user_id exists in JWT but required for model and schema
            new_post = post_schema.load(data_json)
        except ValidationError as e:
            return e.messages, 400

        try:
            new_post.save_to_db()
        except:
            return {'message': 'error while inserting the new post'}, 500
        return post_schema.dump(new_post), 201

    @jwt_required()
    def delete(self, post_id):
        post = PostModel.find_post_by_id(post_id)
        if post:
            post.delete_from_db()
            return {'message': 'post deleted'}
        return {'message': 'no post with such ID'}, 404

    @jwt_required()
    def put(self, post_id):
        # Get info about user.id, user.username, user.password from JWT Token
        user = current_identity

        data_json = request.get_json()

        post = PostModel.find_post_by_id(post_id)

        if post:
            # Update post
            if post.user_id != user.id:
                return {'message': 'you are not author of this post'}

            post.title = data_json.get('title')
            post.content = data_json.get('content')
            post.tag_id = data_json.get('tag_id')
        else:
            # Create new post
            try:
                data_json['user_id'] = user.id
                post = post_schema.load(data_json)
            except ValidationError as e:
                return e.messages, 400

        post.save_to_db()
        return post_schema.dump(post)
