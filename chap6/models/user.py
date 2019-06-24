from werkzeug.security import generate_password_hash

from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    hashed_password = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(80), default="No first name provided.")
    last_name = db.Column(db.String(80), default="No last name provided.")

    def __init__(self, *args, **kwargs):
        self.username = kwargs['username'].strip()
        self.hashed_password = generate_password_hash(kwargs['password'])
        del kwargs['password']
        super(UserModel, self).__init__(*args, **kwargs)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
