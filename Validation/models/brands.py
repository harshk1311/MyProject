from sqlalchemy_continuum import make_versioned
import sqlalchemy as sa
from flask_continuum import VersioningMixin
from db import db
from datetime import datetime
from cerberus import Validator

make_versioned(user_cls=None)
 

class BrandsModel(db.Model,VersioningMixin):
    __versioned__ = {}
    __tablename__ = 'brands'

    brand_id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token             = db.Column(db.Unicode(80))
    brand_name        = db.Column(db.Unicode(255),nullable=True)
    user_id           = db.Column(db.Integer)
    industry_id       = db.Column(db.Integer, db.ForeignKey('industry.industry_id'))
    brand_category_id = db.Column(db.Integer)
    created_by        = db.Column(db.Integer)
    created_on        = db.Column(db.DateTime)
    modified_by       = db.Column(db.Integer)
    modified_on       = db.Column(db.DateTime)
    deleted_by        = db.Column(db.Integer)
    deleted_on        = db.Column(db.DateTime)
    
    industry          = db.relationship('IndustryModel')       

    sa.orm.configure_mappers()

    def __init__(self,brand_name,user_id,industry_id,brand_category_id):
        self.brand_name        = brand_name
        self.user_id           = user_id
        self.industry_id       = industry_id
        self.brand_category_id = brand_category_id


 
    def json(self):
        return{
            'id':self.brand_id,
            'name':self.brand_name,
            'token':self.token
        }

    @classmethod
    def find_by_id(cls, brand_id):
        return cls.query.filter_by(brand_id=brand_id).first()
    
    @classmethod 
    def find_by_name(cls,brand_name):
        return cls.query.filter_by(brand_name=brand_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()


    @classmethod
    def validateData(cls, data, _request):
        
        if _request.method == "POST":
            schema = {'brand_name': {'required': True, 'empty': False, 'type': 'string'},
                      'industry_id': {'required': True, 'empty': False, 'type': 'integer'},
                      'brand_category_id': {'required': True, 'empty': False, 'type': 'integer'}}
        else :
            schema = {'brand_name': {'required': True, 'empty': False, 'type': 'string'}}



        v = Validator(schema)
        v.allow_unknown = True
        return True if(v.validate(data)) else v.errors
