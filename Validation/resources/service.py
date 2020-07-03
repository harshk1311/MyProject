from flask_restful import Resource,reqparse
from models.service import ServiceModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class Service(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('service_name',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('logo',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('brand_id',
                        type=int,
                        
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('category_id',
                        type=int,
                        
                        required=True,
                        help="This field cannot be left blank!"
                        )
    @classmethod
    def get(cls, token):
        try:
            service_id = decodeID(token)
            service = ServiceModel.find_by_id(service_id)
            if not service or service.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return service.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            service_id = decodeID(token)
            service = ServiceModel.find_by_id(service_id)
            if not service or service.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            service.deleted_by =1
            service.deleted_on = datetime.now()
            service.save_to_db()
            #service.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = ServiceModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            service_id = decodeID(token)
            service = ServiceModel.find_by_id(service_id)
            if not service or service.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            service.service_name = data['service_name']
            service.logo = data['logo']
            service.brand_id = data['brand_id']
            service.category_id = data['category_id']
            service.modified_on = datetime.now()
            service.modified_by = 1
            name=data['service_name']
            if name.strip():
                service.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class ServicePost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('service_name',

                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('logo',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('brand_id',
                        type=int,
                        
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('category_id',
                        type=int,
                        
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = self.parser.parse_args()
        service = ServiceModel(**data)
        service.created_by = 1
        service.created_on = datetime.now()
        service.modified_by = 0
        service.deleted_by = 0
        service.modified_on = None
        service.deleted_on =  None
        
        try:
            validateObj = ServiceModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if ServiceModel.find_by_name(data['service_name']):
                return {"success": False, "message": "A service with that Record Name already exists"}, 400
            name=data['service_name']
            if name.strip():
                service.save_to_db()
                service.token = encodeID(service.service_id)
                service.save_to_db()
            else:
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return service.json(), 201