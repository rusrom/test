from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from marsh import mallow

from resources.user import UserRegister
from resources.post import PostList, Post
from resources.tag import TagList, Tag


app = Flask(__name__)

app.secret_key = '$0me_Secret_key'


connection = {
    'user': '**********',
    'database': '**********',
    'host': '**********',
    'password': '***********',
}

dsn = 'mysql+pymysql://{user}:{password}@{host}/{database}'.format(**connection)
app.config['SQLALCHEMY_DATABASE_URI'] = dsn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Create db schemas
@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
jwt = JWT(app, authenticate, identity)

api = Api(app)
api.add_resource(UserRegister, '/user')
api.add_resource(Post, '/post', '/post/<int:post_id>')
api.add_resource(PostList, '/posts')
api.add_resource(Tag, '/tag', '/tag/<string:tag>')
api.add_resource(TagList, '/tags')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    mallow.init_app(app)
    app.run(debug=True, port=8000)
