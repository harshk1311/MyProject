from sqlalchemy_continuum import make_versioned
import sqlalchemy as sa
from flask_continuum import VersioningMixin
from db import db
from datetime import datetime

make_versioned(user_cls=None)


class UserLevelModel(db.Model,VersioningMixin):
    __versioned__ = {}
    __tablename__ = 'userlevel'

    userlevel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level_name  = db.Column(db.Unicode(255))
    user_type_id  = db.Column(db.Integer)
    created_by    = db.Column(db.Integer)
    created_on    = db.Column(db.DateTime)
    modified_by   = db.Column(db.Integer)
    modified_on   = db.Column(db.DateTime)
    deleted_by    = db.Column(db.Integer)
    deleted_on    = db.Column(db.DateTime)

    sa.orm.configure_mappers()

    def __init__(self,level_name,user_type_id):
        self.level_name = level_name
        self.user_type_id = user_type_id
   

    def json(self):
        return{
            'id':self.userlevel_id,
            'name':self.level_name,
            
        }
    
    @classmethod 
    def find_by_name(cls,level_name):
        return cls.query.filter_by(level_name=level_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()


