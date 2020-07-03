from sqlalchemy_continuum import make_versioned
import sqlalchemy as sa
from flask_continuum import VersioningMixin
from db import db
from datetime import datetime
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy.orm import scoped_session, sessionmaker

from cerberus import Validator

make_versioned(user_cls=None)


class UsersModel(db.Model,VersioningMixin):
    __versioned__ = {}
    __tablename__ = 'users'

    user_id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token         = db.Column(db.Unicode(80))
    email            = db.Column(db.Unicode(255))
    password         = db.Column(db.Unicode(55))
    user_type_id       = db.Column(db.Integer)
    company_name      = db.Column(db.Unicode(255))
    first_name        = db.Column(db.Unicode(55))
    last_name         = db.Column(db.Unicode(55))
    phone            = db.Column(db.Unicode(10))
    title            = db.Column(db.Unicode(255))
    owner_manager     = db.Column(db.Unicode(255))
    yearly_budget     = db.Column(db.Integer)
    logo             = db.Column(db.Unicode(255))
    city             = db.Column(db.Unicode(255))
    country_id        = db.Column(db.Integer)
    address          = db.Column(db.Unicode(255))
    timezone         = db.Column(db.Unicode(255))
    level            = db.Column(db.Unicode(255))
    permission       = db.Column(db.Unicode(255))
    assigned_brands   = db.Column(db.Unicode(255))
    assigned_products = db.Column(db.Unicode(255))
    assigned_services = db.Column(db.Unicode(255))
    parent_user_id     = db.Column(db.Integer)
    created_by        = db.Column(db.Integer)
    created_on        = db.Column(db.DateTime)
    modified_by       = db.Column(db.Integer)
    modified_on       = db.Column(db.DateTime)
    deleted_by        = db.Column(db.Integer)
    deleted_on        = db.Column(db.DateTime)

    sa.orm.configure_mappers()

    def __init__(self,email,password,user_type_id,company_name,first_name,last_name,phone,title,owner_manager,yearly_budget,logo,city,country_id,
    address,timezone,level,permission,assigned_brands,assigned_products,assigned_services,parent_user_id) :
        
        self.email =email
        self.password = password
        self.user_type_id = user_type_id
        self.company_name = company_name
        self.first_name = first_name
        self.last_name = last_name 
        self.phone = phone
        self.title = title
        self.owner_manager = owner_manager 
        self.yearly_budget = yearly_budget 
        self.logo = logo
        self.city = city
        self.country_id = country_id 
        self.address = address
        self.timezone = timezone
        self.level = level
        self.permission = permission
        self.assigned_brands = assigned_brands
        self.assigned_products = assigned_products 
        self.assigned_services = assigned_services
        self.parent_user_id = parent_user_id


    @classmethod
    def validateData(cls, data, _request):
        schema = {'email': {'required': True, 'empty': False, 'type': 'string'},
        'password': {'required': True, 'empty': False, 'type': 'string'},
        'user_type_id': {'required': True, 'empty': False, 'type': 'integer'},
        'company_name': {'required': True, 'empty': False, 'type': 'string'},
        'first_name': {'required': True, 'empty': False, 'type': 'string'},
        'last_name': {'required': True, 'empty': False, 'type': 'string'},
        'phone': {'required': True, 'empty': False, 'type': 'integer'},
        'title': {'required': True, 'empty': False, 'type': 'string'},
        'owner_manager': {'required': True, 'empty': False, 'type': 'string'},
        'yearly_budget': {'required': True, 'empty': False, 'type': 'integer'},
        'logo': {'required': True, 'empty': False, 'type': 'string'},
        'city': {'required': True, 'empty': False, 'type': 'string'},
        'country_id': {'required': True, 'empty': False, 'type': 'integer'},
        'address': {'required': True, 'empty': False, 'type': 'string'},
        'timezone': {'required': True, 'empty': False, 'type': 'string'},
        'level': {'required': True, 'empty': False, 'type': 'string'},
        'permission': {'required': True, 'empty': False, 'type': 'string'},
        'assigned_brands': {'required': True, 'empty': False, 'type': 'string'},
        'assigned_products': {'required': True, 'empty': False, 'type': 'string'},
        'assigned_services': {'required': True, 'empty': False, 'type': 'string'},
        'parent_user_id': {'required': True, 'empty': False, 'type': 'integer'},}
        v = Validator(schema)
        v.allow_unknown = True
        return True if(v.validate(data)) else v.errors



    def json(self):
        return{
            'id':self.user_id,
            'name':self.email,
            'token':self.token
        }


    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod 
    def find_by_name(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()


