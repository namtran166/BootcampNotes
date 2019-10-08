from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    hashed_password = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    def __init__(self, *args, **kwargs):
        super(UserModel, self).__init__(*args, **kwargs)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
