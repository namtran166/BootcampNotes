from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    store = db.relationship('StoreModel')

    def __init__(self, *args, **kwargs):
        super(ItemModel, self).__init__(*args, **kwargs)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
