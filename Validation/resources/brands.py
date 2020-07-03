from flask_restful import Resource,reqparse
from models.brands import BrandsModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class Brands(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('brand_name',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('user_id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('industry_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('brand_category_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @classmethod
    def get(cls, token):
        try:
            brand_id = decodeID(token)
            brand = BrandsModel.find_by_id(brand_id)
            if not brand or brand.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return brand.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            brand_id = decodeID(token)
            brand = BrandsModel.find_by_id(brand_id)
            if not brand or brand.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            brand.deleted_by =1
            brand.deleted_on = datetime.now()
            brand.save_to_db()
            #brand.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = BrandsModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            brand_id = decodeID(token)
            brand = BrandsModel.find_by_id(brand_id)
            if not brand or brand.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            brand.brand_name = data['brand_name']
            brand.modified_on = datetime.now()
            brand.modified_by = 1
            brand.user_id = data['user_id']
            brand.industry_id = data['industry_id']
            brand.brand_category_id =data['brand_category_id']
            name=data['brand_name']
            if name.strip():
                brand.save_to_db()
            else :
                return {"success": False, "message":"Brand Name Should not be empty"}
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class BrandsPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('brand_name',
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('industry_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('brand_category_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = self.parser.parse_args()
        brand = BrandsModel(**data)
        brand.created_by = 1
        brand.created_on = datetime.now()
        brand.modified_by = 0
        brand.deleted_by = 0
        brand.modified_on = None
        brand.deleted_on =  None
        
        try:
            validateObj = BrandsModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if BrandsModel.find_by_name(data['brand_name']):
                return {"success": False, "message": "A brand with that Record Name already exists"}, 400
            name=data['brand_name']
            if name.strip():
                brand.save_to_db()
                brand.token = encodeID(brand.brand_id)
                brand.save_to_db()
            else:
                return {"success": False, "message":"Brand Name Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return brand.json(), 201