from db import db


class BookModel(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    author = db.Column(db.String(80))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'))

    store = db.relationship('StoreModel')

    def __init__(self, book_id, name, author, store_id):
        self.book_id = book_id
        self.name = name
        self.author = author
        self.store_id = store_id

    def json(self):
        return {'book_id': self.book_id, 'name': self.name, 'author': self.author, 'store_id': self.store_id}

    @classmethod
    def find_by_book_id(cls, book_id):
        return cls.query.filter_by(book_id=book_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
