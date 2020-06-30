from sqlalchemy_continuum import make_versioned
import sqlalchemy as sa
from flask_continuum import VersioningMixin
from db import db
from datetime import datetime

make_versioned(user_cls=None)


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
        
        self.UserTypeID = UserTypeID
        self.CompanyName = CompanyName
        self.Email = Email
        self.Password = Password
        self.FirstName = FirstName
        self.LastName = LastName
        self.Phone = Phone
        self.Title = Title
        self.OwnerManager = OwnerManager
        self.YearlyBudget = YearlyBudget
        self.Logo = Logo
        self.City = City
        self.CountryID = CountryID
        self.Address = Address
        self.Timezone = Timezone
        self.Level = Level
        self.Permission = Permission
        self.AssignedBrands = AssignedBrands
        self.AssignedProducts = AssignedProducts
        self.AssignedServices = AssignedServices
        self.ParentUserId = ParentUserId
        self.CreatedBy = CreatedBy
        self.CreatedOn = datetime.utcnow()
        self.ModifiedBy = ModifiedBy
        self.ModifiedOn = datetime.utcnow()
        self.DeletedBy = DeletedBy
        self.DeletedOn = datetime.utcnow()
   

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


