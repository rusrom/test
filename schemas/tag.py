from marshmallow import EXCLUDE
from marsh import mallow

from models.tag import TagModel

"""
Because of relationship between PostModel and TagModel
Good idea to import PostModel
"""
from models.post import PostModel
from schemas.post import PostSchema


class TagSchema(mallow.ModelSchema):
    post = mallow.Nested(PostSchema, many=True)

    class Meta:
        model = TagModel
        unknown = EXCLUDE
        dump_only = ('id',)
        include_fk = True
