from flask_restful import Resource,reqparse
from models.language import LanguageModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class Language(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('language_name',
                        
                        required=True,
                        help="This field cannot be left blank!"
                        )
    @classmethod
    def get(cls, token):
        try:
            language_id = decodeID(token)
            language = LanguageModel.find_by_id(language_id)
            if not language or language.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return language.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            language_id = decodeID(token)
            language = LanguageModel.find_by_id(language_id)
            if not language or language.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            language.deleted_by =1
            language.deleted_on = datetime.now()
            language.save_to_db()
            #language.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = LanguageModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            language_id = decodeID(token)
            language = LanguageModel.find_by_id(language_id)
            if not language or language.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            language.language_name = data['language_name']
            language.modified_on = datetime.now()
            language.modified_by = 1
            name=data['language_name']
            if name.strip():
                language.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class LanguagePost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('language_name',
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = self.parser.parse_args()
        language = LanguageModel(**data)
        language.created_by = 1
        language.created_on = datetime.now()
        language.modified_by = 0
        language.deleted_by = 0
        language.modified_on = None
        language.deleted_on =  None
        
        try:
            validateObj = LanguageModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if LanguageModel.find_by_name(data['language_name']):
                return {"success": False, "message": "A language with that Record Name already exists"}, 400
            name=data['language_name']
            if name.strip():
                language.save_to_db()
                language.token = encodeID(language.language_id)
                language.save_to_db()
            else:
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return language.json(), 201