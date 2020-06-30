from sqlalchemy_continuum import make_versioned
import sqlalchemy as sa
from flask_continuum import VersioningMixin
from db import db
from datetime import datetime

make_versioned(user_cls=None)


class ServiceModel(db.Model,VersioningMixin):
    __versioned__ = {}
    __tablename__ = 'service'

    service_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name = db.Column(db.Unicode(255))
    logo          = db.Column(db.Unicode(255))
    brand_id      = db.Column(db.Integer, db.ForeignKey('brands.brand_id'))
    category_id   = db.Column(db.Integer, db.ForeignKey('brandcategory.category_id'))
    created_by    = db.Column(db.Integer)
    created_on    = db.Column(db.DateTime)
    modified_by   = db.Column(db.Integer)
    modified_on   = db.Column(db.DateTime)
    deleted_by    = db.Column(db.Integer)
    deleted_on    = db.Column(db.DateTime)

    brands        = db.relationship('BrandsModel')
    brandcategory = db.relationship('BrandCategoryModel')

    sa.orm.configure_mappers()

    def __init__(self,service_name,logo,brand_id,category_id):
        self.service_name = service_name
        self.logo = logo
        self.brand_id = brand_id
        self.category_id = category_id
   

    def json(self):
        return{
            'id':self.service_id,
            'name':self.service_name,
            'logo':self.logo
            
        }
    
    @classmethod 
    def find_by_name(cls,service_name):
        return cls.query.filter_by(service_name=service_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()