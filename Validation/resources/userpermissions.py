from flask_restful import Resource,reqparse
from models.userpermissions import UserPermissionModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class UserPermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('section_name',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('feature_name',
                        
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
            permission_id = decodeID(token)
            permission = UserPermissionModel.find_by_id(permission_id)
            if not permission or permission.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return permission.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            permission_id = decodeID(token)
            permission = UserPermissionModel.find_by_id(permission_id)
            if not permission or permission.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            permission.deleted_by =1
            permission.deleted_on = datetime.now()
            permission.save_to_db()
            #permission.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = UserPermissionModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            permission_id = decodeID(token)
            permission = UserPermissionModel.find_by_id(permission_id)
            if not permission or permission.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            permission.section_name = data['section_name']
            permission.feature_name = data['feature_name']
            permission.user_type_id = data['user_type_id']
            permission.modified_on = datetime.now()
            permission.modified_by = 1
            name=data['section_name']
            if name.strip():
                permission.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class UserPermissionPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('section_name',

                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('feature_name',
                        
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
        permission = UserPermissionModel(**data)
        permission.created_by = 1
        permission.created_on = datetime.now()
        permission.modified_by = 0
        permission.deleted_by = 0
        permission.modified_on = None
        permission.deleted_on =  None
        
        try:
            validateObj = UserPermissionModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if UserPermissionModel.find_by_name(data['section_name']):
                return {"success": False, "message": "A permission with that Record Name already exists"}, 400
            name=data['section_name']
            if name.strip():
                permission.save_to_db()
                permission.token = encodeID(permission.permission_id)
                permission.save_to_db()
            else:
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return permission.json(), 201