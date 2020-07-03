from flask_restful import Resource,reqparse
from models.gender import  GenderModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class Gender(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('gender_name',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    @classmethod
    def get(cls, token):
        try:
            gender_id = decodeID(token)
            gender = GenderModel.find_by_id(gender_id)
            if not gender or gender.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return gender.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            gender_id = decodeID(token)
            gender = GenderModel.find_by_id(gender_id)
            if not gender or gender.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            gender.deleted_by =1
            gender.deleted_on = datetime.now()
            gender.save_to_db()
            #gender.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = GenderModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            gender_id = decodeID(token)
            gender = GenderModel.find_by_id(gender_id)
            if not gender or gender.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            gender.gender_name = data['gender_name']
            gender.modified_on = datetime.now()
            gender.modified_by = 1
            gender.save_to_db()
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class GenderPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('gender_name',
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = self.parser.parse_args()
        gender = GenderModel(**data)
        gender.created_by = 1
        gender.created_on = datetime.now()
        gender.modified_by = 0
        gender.deleted_by = 0
        gender.modified_on = None
        gender.deleted_on =  None
        
        try:
            validateObj = GenderModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if GenderModel.find_by_name(data['gender_name']):
                return {"success": False, "message": "A gender with that Record Name already exists"}, 400
            name=data['gender_name']
            if name.strip():
                gender.save_to_db()
                gender.token = encodeID(gender.gender_id)
                gender.save_to_db()
            else:
                return {"success": False, "message":"Brand Name Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return gender.json(), 201