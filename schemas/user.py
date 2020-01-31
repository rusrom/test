from marshmallow import EXCLUDE
from marsh import mallow
from models.user import UserModel


class UserSchema(mallow.ModelSchema):
    class Meta:
        model = UserModel
        unknown = EXCLUDE
        load_only = ('password',)
        dump_only = ('id',)
