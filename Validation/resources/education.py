from flask_restful import Resource,reqparse
from models.education import EducationModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class Education(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('education_name',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    @classmethod
    def get(cls, token):
        try:
            education_id = decodeID(token)
            education = EducationModel.find_by_id(education_id)
            if not education or education.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return education.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            education_id = decodeID(token)
            education = EducationModel.find_by_id(education_id)
            if not education or education.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            education.deleted_by =1
            education.deleted_on = datetime.now()
            education.save_to_db()
            #education.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = EducationModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            education_id = decodeID(token)
            education = EducationModel.find_by_id(education_id)
            if not education or education.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            education.education_name = data['education_name']
            education.modified_on = datetime.now()
            education.modified_by = 1
            name=data['education_name']
            if name.strip():
                education.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class EducationPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('education_name',
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = self.parser.parse_args()
        education = EducationModel(**data)
        education.created_by = 1
        education.created_on = datetime.now()
        education.modified_by = 0
        education.deleted_by = 0
        education.modified_on = None
        education.deleted_on =  None
        
        try:
            validateObj = EducationModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if EducationModel.find_by_name(data['education_name']):
                return {"success": False, "message": "A education with that Record Name already exists"}, 400
            name=data['education_name']
            if name.strip():
                education.save_to_db()
                education.token = encodeID(education.education_id)
                education.save_to_db()
            else:
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return education.json(), 201