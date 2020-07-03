from flask_restful import Resource,reqparse
from models.industry import IndustryModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class Industry(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('industry_name',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    @classmethod
    def get(cls, token):
        try:
            industry_id = decodeID(token)
            industry = IndustryModel.find_by_id(industry_id)
            if not industry or industry.token != token:
                return {"success": False, 'message': 'Industry Not Found'}, 404
            return industry.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            industry_id = decodeID(token)
            industry = IndustryModel.find_by_id(industry_id)
            if not industry or industry.token != token:
                return {"success": False, 'message': 'Industry Not Found'}, 404
            industry.deleted_by =1
            industry.deleted_on = datetime.now()
            industry.save_to_db()
            #industry.delete_from_db()
            
            return {"success": True, 'message': 'Industry deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = request.get_json()
            validateObj = IndustryModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            industry_id = decodeID(token)
            industry = IndustryModel.find_by_id(industry_id)
            if not industry or industry.token != token:
                return {"success": False, 'message': 'User Not Found'}, 404
            
                
            industry.industry_name = data['industry_name']
            industry.modified_on = datetime.now()
            industry.modified_by = 1
            name=data['industry_name']
            if name.strip():
                industry.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "User updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class IndustryPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('industry_name',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = self.parser.parse_args()
        industry = IndustryModel(**data)
        industry.created_by = 1
        industry.created_on = datetime.now()
        industry.modified_by = 0
        industry.deleted_by = 0
        industry.modified_on = None
        industry.deleted_on =  None
        
        try:
            validateObj = IndustryModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if IndustryModel.find_by_name(data['industry_name']):
                return {"success": False, "message": "A industry with that Industry Name already exists"}, 400
            name=data['industry_name']
            if name.strip():
                industry.save_to_db()
                industry.token = encodeID(industry.industry_id)
                industry.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return industry.json(), 201