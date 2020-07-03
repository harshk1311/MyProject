from flask_restful import Resource,reqparse
from models.userlevel import UserLevelModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class UserLevel(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('level_name',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('user_type_id',
                        type=int,
                        
                        required=True,
                        help="This field cannot be left blank!"
                        )
                        
    @classmethod
    def get(cls, token):
        try:
            userlevel_id = decodeID(token)
            userlevel = UserLevelModel.find_by_id(userlevel_id)
            if not userlevel or userlevel.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return userlevel.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            userlevel_id = decodeID(token)
            userlevel = UserLevelModel.find_by_id(userlevel_id)
            if not userlevel or userlevel.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            userlevel.deleted_by =1
            userlevel.deleted_on = datetime.now()
            userlevel.save_to_db()
            #userlevel.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = UserLevelModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            userlevel_id = decodeID(token)
            userlevel = UserLevelModel.find_by_id(userlevel_id)
            if not userlevel or userlevel.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            userlevel.level_name = data['level_name']
            userlevel.user_type_id = data['user_type_id']
            userlevel.modified_on = datetime.now()
            userlevel.modified_by = 1
            name=data['level_name']
            if name.strip():
                userlevel.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class UserLevelPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('level_name',

                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('user_type_id',
                        type=int,
                        
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = self.parser.parse_args()
        userlevel = UserLevelModel(**data)
        userlevel.created_by = 1
        userlevel.created_on = datetime.now()
        userlevel.modified_by = 0
        userlevel.deleted_by = 0
        userlevel.modified_on = None
        userlevel.deleted_on =  None
        
        try:
            validateObj = UserLevelModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if UserLevelModel.find_by_name(data['level_name']):
                return {"success": False, "message": "A userlevel with that Record Name already exists"}, 400
            name=data['level_name']
            if name.strip():
                userlevel.save_to_db()
                userlevel.token = encodeID(userlevel.userlevel_id)
                userlevel.save_to_db()
            else:
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return userlevel.json(), 201