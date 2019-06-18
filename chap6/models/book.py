from db import db

class BookModel(db.Model):
    __tablename__ = 'books'

    bookID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    author = db.Column(db.String(80))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.storeID'))

    store = db.relationship('StoreModel')

    def __init__(self, bookID, name, author, store_id):
        self.bookID = bookID
        self.name = name
        self.author = author
        self.store_id = store_id

    def json(self):
        return {'bookID': self.bookID, 'name': self.name, 'author': self.author, 'store_id': self.store_id}

    @classmethod
    def find_by_bookID(cls, bookID):
        return cls.query.filter_by(bookID = bookID).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
