from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from models.tag import TagModel
from schemas.tag import TagSchema


tag_schema = TagSchema()
tag_list_schema = TagSchema(many=True)


class Tag(Resource):
    def get(self, tag):
        tag = TagModel.find_by_name(tag)
        if tag:
            return {'tag': tag_schema.dump(tag)}
        return {'message': 'no such tag'}, 404

    def post(self):
        try:
            json_data = request.get_json()
            new_tag = tag_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 400

        if TagModel.find_by_name(new_tag.tag):
            return {'message': f'tag #{new_tag.tag} already exists'}, 400

        new_tag.save_to_db()
        return tag_schema.dump(new_tag), 201

    def delete(self, tag):
        tag = TagModel.find_by_name(tag)
        if tag:
            tag.delete_from_db()
            return {'message': f'tag #{tag.tag} was deleted'}
        return {'message': 'no such tag'}


class TagList(Resource):
    def get(self):
        return {'tags': tag_list_schema.dump(TagModel.query.all())}
