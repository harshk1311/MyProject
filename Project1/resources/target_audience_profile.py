from flask_restful import Resource,reqparse
from models.target_audience_profile import TargetAudienceProfileModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class TargetAudienceProfile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('business',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('age_group_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('gender_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('target_languages',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_nationality',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_education',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_occupation',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_interest',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def get(self, audience_profile_name):
        audience_profile = TargetAudienceProfileModel.find_by_name(audience_profile_name)
        try :
            if audience_profile:
                return audience_profile.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    def put(self, audience_profile_name):
        data = self.parser.parse_args()
        audience_profile=TargetAudienceProfileModel.find_by_name(audience_profile_name)
        if audience_profile:
            audience_profile.business = data['business']
            audience_profile.age_group_id = data['age_group_id']
            audience_profile.gender_id = data['gender_id']
            audience_profile.target_languages = data['target_languages']
            audience_profile.target_nationality = data['target_nationality']
            audience_profile.target_education = data['target_education']
            audience_profile.target_occupation = data['target_occupation']
            audience_profile.target_interest = data['target_interest']
            audience_profile.modified_on = datetime.now()
            audience_profile.modified_by = 1
        else :
            return {"Message":"Record Not FOUND"}
        audience_profile.save_to_db()
        return audience_profile.json()
    @classmethod
    def delete(cls, audience_profile_name):
        audience_profile = TargetAudienceProfileModel.find_by_name(audience_profile_name)
        if audience_profile:
            audience_profile.deleted_by =1
            audience_profile.deleted_on = datetime.now()
            audience_profile.save_to_db()
            #audience_profile.delete_from_db()
            return {'message': 'Record deleted'}
            
            
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, audience_profile_name):
        db.create_all()
        db.session.commit()
        if TargetAudienceProfileModel.find_by_name(audience_profile_name):
            return {'message': "An Record with name '{}' already exists.".format(audience_profile_name)}, 400

        data = self.parser.parse_args()
        
        
        audience_profile = TargetAudienceProfileModel(audience_profile_name,**data,)
        audience_profile.created_by = 1
        audience_profile.created_on = datetime.now()
        audience_profile.modified_by = 0
        audience_profile.deleted_by = 0
        try:
            
            audience_profile.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
            
        return audience_profile.json(), 201