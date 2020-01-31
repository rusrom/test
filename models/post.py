from db import db


class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    tag = db.relationship('TagModel')


    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'tag_id': self.tag_id,
        }

    @classmethod
    def find_post_by_id(cls, post_id):
        return cls.query.filter_by(id=post_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
