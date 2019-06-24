from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    store_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(StoreModel, self).__init__(*args, **kwargs)

    def json(self):
        return {
            'id': self.store_id,
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_store_id(cls, _id):
        return cls.query.filter_by(store_id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
