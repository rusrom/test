from db import db


class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(30), nullable=False)

    posts = db.relationship('PostModel', lazy='dynamic')

    @classmethod
    def find_by_name(cls, tag):
        return cls.query.filter_by(tag=tag).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
