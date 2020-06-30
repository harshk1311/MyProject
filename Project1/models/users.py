from sqlalchemy_continuum import make_versioned
import sqlalchemy as sa
from flask_continuum import VersioningMixin
from db import db
from datetime import datetime
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
make_versioned(user_cls=None)

engine = create_engine('postgresql://postgres:oracle@localhost/projec_db', echo = True)
class UsersModel(db.Model,VersioningMixin):
    __versioned__ = {}
    __tablename__ = 'users'

    user_id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    def __init__(self,email,password,user_type_id,company_name,first_name,last_name,phone,title,owner_manager,yearly_budget,logo,city,country_id,address,timezone,level,permission,assigned_brands,assigned_products,assigned_services,parent_user_id) :
        
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


   

    def json(self):
        return{
            'id':self.user_id,
            'name':self.email
        }
    
    @classmethod 
    def find_by_Email(cls,email):
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


