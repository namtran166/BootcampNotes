from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'))

    store = db.relationship('StoreModel')

    def __init__(self, item_id, name, author, store_id):
        self.item_id = item_id
        self.name = name
        self.price = author
        self.store_id = store_id

    def json(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'author': self.author,
            'store_id': self.store_id
        }

    @classmethod
    def find_by_item_id(cls, item_id):
        return cls.query.filter_by(item_id=item_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
