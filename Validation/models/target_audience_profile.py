from sqlalchemy_continuum import make_versioned
import sqlalchemy as sa
from flask_continuum import VersioningMixin
from db import db
from datetime import datetime
from cerberus import Validator

make_versioned(user_cls=None)


class TargetAudienceProfileModel(db.Model,VersioningMixin):
    __versioned__ = {}
    __tablename__ = 'target_audience_profile'

    target_audience_profile_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token         = db.Column(db.Unicode(80))
    audience_profile_name = db.Column(db.Unicode(255))
    business = db.Column(db.Unicode(255))
    age_group_id = db.Column(db.Integer, db.ForeignKey('age_group.age_group_id'))
    gender_id  = db.Column(db.Integer, db.ForeignKey('gender.gender_id'))
    target_languages = db.Column(db.Unicode(255))
    target_nationality = db.Column(db.Unicode(255))
    target_education = db.Column(db.Unicode(255))
    target_occupation = db.Column(db.Unicode(255))
    target_interest = db.Column(db.Unicode(255))
    created_by    = db.Column(db.Integer)
    created_on    = db.Column(db.DateTime)
    modified_by   = db.Column(db.Integer)
    modified_on   = db.Column(db.DateTime)
    deleted_by    = db.Column(db.Integer)
    deleted_on    = db.Column(db.DateTime)

    agegroup        = db.relationship('AgeGroupModel')
    gender          = db.relationship('GenderModel')
    sa.orm.configure_mappers()

    def __init__(self,audience_profile_name,business,age_group_id,gender_id,target_languages,target_nationality,target_education,target_occupation,target_interest):
        self.audience_profile_name = audience_profile_name
        self.business = business
        self.age_group_id = age_group_id
        self.gender_id = gender_id
        self.target_languages = target_languages
        self.target_nationality = target_nationality
        self.target_education = target_education
        self.target_occupation = target_occupation
        self.target_interest = target_interest
   

    def json(self):
        return{
            'id':self.target_audience_profile_id,
            'name':self.audience_profile_name,
            'token' : self.token
        }


    @classmethod
    def find_by_id(cls, target_audience_profile_id):
        return cls.query.filter_by(target_audience_profile_id=target_audience_profile_id).first()

    @classmethod 
    def find_by_name(cls,audience_profile_name):
        return cls.query.filter_by(audience_profile_name=audience_profile_name).first()

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
        schema = {'audience_profile_name': {'required': True, 'empty': False, 'type': 'string'},
        'business': {'required': True, 'empty': False, 'type': 'string'},
        'age_group_id': {'required': True, 'empty': False, 'type': 'integer'},
        'gender_id': {'required': True, 'empty': False, 'type': 'integer'},
        'target_languages': {'required': True, 'empty': False, 'type': 'string'},
        'target_nationality': {'required': True, 'empty': False, 'type': 'string'},
        'target_education': {'required': True, 'empty': False, 'type': 'string'},
        'target_occupation': {'required': True, 'empty': False, 'type': 'string'},
        'target_interest': {'required': True, 'empty': False, 'type': 'string'}}
        v = Validator(schema)
        v.allow_unknown = True
        return True if(v.validate(data)) else v.errors