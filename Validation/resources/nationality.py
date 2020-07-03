from flask_restful import Resource,reqparse
from models.nationality import NationalityModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class Nationality(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nationality_name',
                        
                        required=True,
                        help="This field cannot be left blank!"
                        )
    @classmethod
    def get(cls, token):
        try:
            nationality_id = decodeID(token)
            nationality = NationalityModel.find_by_id(nationality_id)
            if not nationality or nationality.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return nationality.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            nationality_id = decodeID(token)
            nationality = NationalityModel.find_by_id(nationality_id)
            if not nationality or nationality.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            nationality.deleted_by =1
            nationality.deleted_on = datetime.now()
            nationality.save_to_db()
            #nationality.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = NationalityModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            nationality_id = decodeID(token)
            nationality = NationalityModel.find_by_id(nationality_id)
            if not nationality or nationality.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            nationality.nationality_name = data['nationality_name']
            nationality.modified_on = datetime.now()
            nationality.modified_by = 1
            name=data['nationality_name']
            if name.strip():
                nationality.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class NationalityPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nationality_name',
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = self.parser.parse_args()
        nationality = NationalityModel(**data)
        nationality.created_by = 1
        nationality.created_on = datetime.now()
        nationality.modified_by = 0
        nationality.deleted_by = 0
        nationality.modified_on = None
        nationality.deleted_on =  None
        
        try:
            validateObj = NationalityModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if NationalityModel.find_by_name(data['nationality_name']):
                return {"success": False, "message": "A nationality with that Record Name already exists"}, 400
            name=data['nationality_name']
            if name.strip():
                nationality.save_to_db()
                nationality.token = encodeID(nationality.nationality_id)
                nationality.save_to_db()
            else:
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return nationality.json(), 201