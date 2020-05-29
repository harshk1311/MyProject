from db import db


class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80))
    description=db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    quantity=db.Column(db.Integer)

    cid = db.Column(db.Integer, db.ForeignKey('categories.cid'))
    category = db.relationship('CategoryModel')

    def __init__(self, id, cid, name,description,price,quantity):
        self.id=id
        self.cid=cid
        self.name = name
        self.description=description
        self.price = price
        self.quantity=quantity

    def json(self):
        return {
            'id': self.id,
            'cid':self.cid,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
