from sqlalchemy_continuum import make_versioned
import sqlalchemy as sa
from flask_continuum import VersioningMixin
from db import db
from datetime import datetime

make_versioned(user_cls=None)


class BrandCategoryModel(db.Model,VersioningMixin):
    __versioned__ = {}
    __tablename__ = 'brandcategory'

    category_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.Unicode(255))
    logo          = db.Column(db.Unicode(255))
    created_by    = db.Column(db.Integer)
    created_on    = db.Column(db.DateTime)
    modified_by   = db.Column(db.Integer)
    modified_on   = db.Column(db.DateTime)
    deleted_by    = db.Column(db.Integer)
    deleted_on    = db.Column(db.DateTime)

    sa.orm.configure_mappers()

    def __init__(self,category_name,logo):
        self.category_name = category_name
        self.logo = logo
   

    def json(self):
        return{
            'id':self.category_id,
            'name':self.category_name,
            
        }
    
    @classmethod 
    def find_by_name(cls,category_name):
        return cls.query.filter_by(category_name=category_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()


