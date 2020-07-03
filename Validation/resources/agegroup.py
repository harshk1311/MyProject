from flask_restful import Resource,reqparse
from models.agegroup import AgeGroupModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class AgeGroup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('age_group',
                        type=str,
                        trim=True,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @classmethod
    def get(cls, token):
        try:
            age_group_id = decodeID(token)
            age_group = AgeGroupModel.find_by_id(age_group_id)
            if not age_group or age_group.token != token:
                return {"success": False, 'message': 'Industry Not Found'}, 404
            return age_group.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            age_group_id = decodeID(token)
            age_group = AgeGroupModel.find_by_id(age_group_id)
            if not age_group or age_group.token != token:
                return {"success": False, 'message': 'Industry Not Found'}, 404
            age_group.deleted_by =1
            age_group.deleted_on = datetime.now()
            age_group.save_to_db()
            #age_group.delete_from_db()
            return {"success": True, 'message': 'Industry deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = AgeGroupModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            age_group_id = decodeID(token)
            age_group = AgeGroupModel.find_by_id(age_group_id)
            if not age_group or age_group.token != token:
                return {"success": False, 'message': 'Industry Not Found'}, 404
            age_group.modified_by = 1
            age_group.modified_at = datetime.now()
            age_group.age_group = data['age_group']
            name=data['age_group']
            if name.strip():
                age_group.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "Industry updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}

class AgeGroupPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('age_group',
                        type=str,
                        trim=True,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = self.parser.parse_args()
        age_group = AgeGroupModel(**data)
        age_group.created_by = 1
        age_group.created_on = datetime.now()
        age_group.modified_by = 0
        age_group.deleted_by = 0
        age_group.modified_on = None
        age_group.deleted_on =  None
        
        try:
            validateObj = AgeGroupModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if AgeGroupModel.find_by_name(data['age_group']):
                return {"success": False, "message": "A age_group with that  Name already exists"}, 400
            name=data['age_group']
            if name.strip():
                age_group.save_to_db()
                age_group.token = encodeID(age_group.age_group_id)
                age_group.save_to_db()
            else:
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return age_group.json(), 201