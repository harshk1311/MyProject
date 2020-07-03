from flask_restful import Resource,reqparse
from models.occupation import OccupationModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class Occupation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('occupation_name',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    @classmethod
    def get(cls, token):
        try:
            occupation_id = decodeID(token)
            occupation = OccupationModel.find_by_id(occupation_id)
            if not occupation or occupation.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return occupation.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            occupation_id = decodeID(token)
            occupation = OccupationModel.find_by_id(occupation_id)
            if not occupation or occupation.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            occupation.deleted_by =1
            occupation.deleted_on = datetime.now()
            occupation.save_to_db()
            #occupation.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = OccupationModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            occupation_id = decodeID(token)
            occupation = OccupationModel.find_by_id(occupation_id)
            if not occupation or occupation.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            occupation.occupation_name = data['occupation_name']
            occupation.modified_on = datetime.now()
            occupation.modified_by = 1
            name=data['occupation_name']
            if name.strip():
                occupation.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class OccupationPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('occupation_name',
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = self.parser.parse_args()
        occupation = OccupationModel(**data)
        occupation.created_by = 1
        occupation.created_on = datetime.now()
        occupation.modified_by = 0
        occupation.deleted_by = 0
        occupation.modified_on = None
        occupation.deleted_on =  None
        
        try:
            validateObj = OccupationModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if OccupationModel.find_by_name(data['occupation_name']):
                return {"success": False, "message": "A occupation with that Record Name already exists"}, 400
            name=data['occupation_name']
            if name.strip():
                occupation.save_to_db()
                occupation.token = encodeID(occupation.occupation_id)
                occupation.save_to_db()
            else:
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return occupation.json(), 201