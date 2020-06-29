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

    UserID           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserTypeID       = db.Column(db.Integer)
    CompanyName      = db.Column(db.Unicode(255))
    Email            = db.Column(db.Unicode(255))
    Password         = db.Column(db.Unicode(55))
    FirstName        = db.Column(db.Unicode(55))
    LastName         = db.Column(db.Unicode(55))
    Phone            = db.Column(db.Unicode(10))
    Title            = db.Column(db.Unicode(255))
    OwnerManager     = db.Column(db.Unicode(255))
    YearlyBudget     = db.Column(db.Integer)
    Logo             = db.Column(db.Unicode(255))
    City             = db.Column(db.Unicode(255))
    CountryID        = db.Column(db.Integer)
    Address          = db.Column(db.Unicode(255))
    Timezone         = db.Column(db.Unicode(255))
    Level            = db.Column(db.Unicode(255))
    Permission       = db.Column(db.Unicode(255))
    AssignedBrands   = db.Column(db.Unicode(255))
    AssignedProducts = db.Column(db.Unicode(255))
    AssignedServices = db.Column(db.Unicode(255))
    ParentUserId     = db.Column(db.Integer)
    CreatedBy        = db.Column(db.Integer,default=u'NULL')
    CreatedOn        = db.Column(db.DateTime,server_default=db.func.now())
    ModifiedBy       = db.Column(db.Integer,default=u'NULL')
    ModifiedOn       = db.Column(db.DateTime,server_default=db.func.now(), server_onupdate=db.func.now())
    DeletedBy        = db.Column(db.Integer,default=u'NULL')
    DeletedOn        = db.Column(db.DateTime,server_default=db.func.now())

    sa.orm.configure_mappers()

    def __init__(self,UserTypeID,CompanyName,Email,Password,FirstName,LastName,Phone,Title,OwnerManager,YearlyBudget,Logo,City,CountryID,Address,Timezone,Level,Permission,AssignedBrands,AssignedProducts,AssignedServices,ParentUserId,CreatedBy,CreatedOn,ModifiedBy,ModifiedOn,DeletedBy,DeletedOn) :
        
        self.Email = Email
        self.Password = Password
        
   

    def json(self):
        return{
            'id':self.IndustryID,
            'name':self.IndustryName
        }
    
    @classmethod 
    def find_by_Email(cls,Email):
        return cls.query.filter_by(Email=Email).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()


