from marshmallow import EXCLUDE
from marsh import mallow

from models.post import PostModel

"""
Because of relationship between PostModel and TagModel
Good idea to import TagModel
"""
from models.tag import TagModel


class PostSchema(mallow.ModelSchema):
    class Meta:
        model = PostModel
        unknown = EXCLUDE
        load_only = ('tag',)  # tag is relationship field in PostModel
        dump_only = ('id',)
        include_fk = True
