from sqlalchemy_continuum import make_versioned
import sqlalchemy as sa
from flask_continuum import VersioningMixin
from db import db
from datetime import datetime
from cerberus import Validator


make_versioned(user_cls=None)


class OccupationModel(db.Model,VersioningMixin):
    __versioned__ = {}
    __tablename__ = 'occupation'

    occupation_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token         = db.Column(db.Unicode(80))
    occupation_name = db.Column(db.Unicode(255))
    created_by    = db.Column(db.Integer)
    created_on    = db.Column(db.DateTime)
    modified_by   = db.Column(db.Integer)
    modified_on   = db.Column(db.DateTime)
    deleted_by    = db.Column(db.Integer)
    deleted_on    = db.Column(db.DateTime)


    sa.orm.configure_mappers()

    def __init__(self,occupation_name):
        self.occupation_name = occupation_name
   

    def json(self):
        return{
            'id':self.occupation_id,
            'name':self.occupation_name,
            'token':self.token
        }

    @classmethod
    def find_by_id(cls, occupation_id):
        return cls.query.filter_by(occupation_id=occupation_id).first()

    @classmethod 
    def find_by_name(cls,occupation_name):
        return cls.query.filter_by(occupation_name=occupation_name).first()

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
        schema = {'occupation_name': {'required': True, 'empty': False, 'type': 'string'}}
        v = Validator(schema)
        v.allow_unknown = True
        return True if(v.validate(data)) else v.errors