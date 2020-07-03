from flask_restful import Resource,reqparse
from models.users import UsersModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class Users(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('user_type_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('company_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('phone',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('owner_manager',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('yearly_budget',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )



    parser.add_argument('logo',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('city',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('country_id',
                        type=int,
                        required=True,
                        
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('address',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('timezone',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('level',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('permission',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('assigned_brands',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('assigned_products',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('assigned_services',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('parent_user_id',
                        type=int,
                        required=True,

                        help="This field cannot be left blank!"
                        )
                        
    @classmethod
    def get(cls, token):
        try:
            user_id = decodeID(token)
            user = UsersModel.find_by_id(user_id)
            if not user or user.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return user.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            user_id = decodeID(token)
            user = UsersModel.find_by_id(user_id)
            if not user or user.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            user.deleted_by =1
            user.deleted_on = datetime.now()
            user.save_to_db()
            #user.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = UsersModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            user_id = decodeID(token)
            user = UsersModel.find_by_id(user_id)
            if not user or user.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            user.modified_on = datetime.now()
            user.modified_by = 1
            user.password = data['password']
            user.user_type_id = data['user_type_id']
            user.company_name = data['company_name']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.phone = data['phone']
            user.title = data['title']
            user.owner_manager = data['owner_manager']
            user.yearly_budget = data['yearly_budget']
            user.logo = data['logo']
            user.city = data['city']
            user.country_id = data['country_id']
            user.address = data['address']
            user.timezone = data['timezone']
            user.level = data['level']
            user.permission = data['permission']
            user.assigned_brands = data['assigned_brands']
            user.assigned_products = data['assigned_products']
            user.assigned_services = data['assigned_services']
            user.parent_user_id = data['parent_user_id']
            name=data['email']
            if name.strip():
                user.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class UsersPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',

                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('user_type_id',
                        type=int,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('company_name',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('phone',
                        type=int,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('title',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('owner_manager',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('yearly_budget',
                        type=int,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )



    parser.add_argument('logo',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('city',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('country_id',
                        type=int,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('address',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('timezone',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('level',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('permission',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('assigned_brands',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('assigned_products',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('assigned_services',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('parent_user_id',
                        type=int,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = self.parser.parse_args()
        user = UsersModel(**data)
        user.created_by = 1
        user.created_on = datetime.now()
        user.modified_by = 0
        user.deleted_by = 0
        user.modified_on = None
        user.deleted_on =  None
        
        try:
            validateObj = UsersModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if UsersModel.find_by_name(data['email']):
                return {"success": False, "message": "A user with that Record Name already exists"}, 400
            name=data['email']
            if name.strip():
                user.save_to_db()
                user.token = encodeID(user.user_id)
                user.save_to_db()
            else:
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return user.json(), 201