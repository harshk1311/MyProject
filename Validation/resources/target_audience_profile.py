from flask_restful import Resource,reqparse
from models.target_audience_profile import TargetAudienceProfileModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class TargetAudienceProfile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('audience_profile_name',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('business',
                        type=str,
                        required=True,
                        trim=True,
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
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_nationality',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_education',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_occupation',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_interest',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    @classmethod
    def get(cls, token):
        try:
            target_audience_profile_id = decodeID(token)
            audience_profile = TargetAudienceProfileModel.find_by_id(target_audience_profile_id)
            if not audience_profile or audience_profile.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return audience_profile.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            target_audience_profile_id = decodeID(token)
            audience_profile = TargetAudienceProfileModel.find_by_id(target_audience_profile_id)
            if not audience_profile or audience_profile.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            audience_profile.deleted_by =1
            audience_profile.deleted_on = datetime.now()
            audience_profile.save_to_db()
            #audience_profile.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = TargetAudienceProfileModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            target_audience_profile_id = decodeID(token)
            audience_profile = TargetAudienceProfileModel.find_by_id(target_audience_profile_id)
            if not audience_profile or audience_profile.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            audience_profile.audience_profile_name = data['audience_profile_name']
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
            name=data['audience_profile_name']
            if name.strip():
                audience_profile.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class TargetAudienceProfilePost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('audience_profile_name',

                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('business',
                        type=str,
                        required=True,
                        trim=True,
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
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_nationality',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_education',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_occupation',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_interest',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = self.parser.parse_args()
        audience_profile = TargetAudienceProfileModel(**data)
        audience_profile.created_by = 1
        audience_profile.created_on = datetime.now()
        audience_profile.modified_by = 0
        audience_profile.deleted_by = 0
        audience_profile.modified_on = None
        audience_profile.deleted_on =  None
        
        try:
            validateObj = TargetAudienceProfileModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if TargetAudienceProfileModel.find_by_name(data['audience_profile_name']):
                return {"success": False, "message": "A audience_profile with that Record Name already exists"}, 400
            name=data['audience_profile_name']
            if name.strip():
                audience_profile.save_to_db()
                audience_profile.token = encodeID(audience_profile.target_audience_profile_id)
                audience_profile.save_to_db()
            else:
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return audience_profile.json(), 201