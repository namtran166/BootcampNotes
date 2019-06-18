from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    storeID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    books = db.relationship('BookModel', lazy = 'dynamic')

    def __init__(self, storeID, name):
        self.storeID = storeID
        self.name = name

    def json(self):
        return {
            'storeID': self.storeID,
            'name': self.name,
            'books': [book.json() for book in self.books.all()]
        }

    @classmethod
    def find_by_storeID(cls, storeID):
        return cls.query.filter_by(storeID = storeID).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
