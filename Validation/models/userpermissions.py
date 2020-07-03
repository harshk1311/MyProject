from sqlalchemy_continuum import make_versioned
import sqlalchemy as sa
from flask_continuum import VersioningMixin
from db import db
from datetime import datetime
from cerberus import Validator


make_versioned(user_cls=None)


class UserPermissionModel(db.Model,VersioningMixin):
    __versioned__ = {}
    __tablename__ = 'userpermissions'

    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token         = db.Column(db.Unicode(80))
    section_name  = db.Column(db.Unicode(255))
    feature_name  = db.Column(db.Unicode(255))
    user_type_id  = db.Column(db.Integer)
    created_by    = db.Column(db.Integer)
    created_on    = db.Column(db.DateTime)
    modified_by   = db.Column(db.Integer)
    modified_on   = db.Column(db.DateTime)
    deleted_by    = db.Column(db.Integer)
    deleted_on    = db.Column(db.DateTime)

    sa.orm.configure_mappers()

    def __init__(self,section_name,feature_name,user_type_id):
        self.section_name = section_name
        self.feature_name = feature_name
        self.user_type_id = user_type_id
   

    def json(self):
        return{
            'id':self.permission_id,
            'name':self.section_name,
            'feature_name':self.feature_name,
            'tokn':self.token
        }


    @classmethod
    def find_by_id(cls, permission_id):
        return cls.query.filter_by(permission_id=permission_id).first()
    
    @classmethod 
    def find_by_name(cls,section_name):
        return cls.query.filter_by(section_name=section_name).first()

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
        schema = {'section_name': {'required': True, 'empty': False, 'type': 'string'},
        'feature_name': {'required': True, 'empty': False, 'type': 'string'},
        'user_type_id': {'required': True, 'empty': False, 'type': 'integer'}}
        v = Validator(schema)
        v.allow_unknown = True
        return True if(v.validate(data)) else v.errors


