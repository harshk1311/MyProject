from flask_restful import Resource,reqparse
from models.products import ProductsModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class Products(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_name',
                        
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
            product_id = decodeID(token)
            product = ProductsModel.find_by_id(product_id)
            if not product or product.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return product.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            product_id = decodeID(token)
            product = ProductsModel.find_by_id(product_id)
            if not product or product.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            product.deleted_by =1
            product.deleted_on = datetime.now()
            product.save_to_db()
            #product.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = ProductsModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            product_id = decodeID(token)
            product = ProductsModel.find_by_id(product_id)
            if not product or product.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            product.product_name = data['product_name']
            product.logo = data['logo']
            product.brand_id = data['brand_id']
            product.category_id = data['category_id']
            product.modified_on = datetime.now()
            product.modified_by = 1
            name=data['product_name']
            if name.strip():
                product.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class ProductsPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_name',

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
        product = ProductsModel(**data)
        product.created_by = 1
        product.created_on = datetime.now()
        product.modified_by = 0
        product.deleted_by = 0
        product.modified_on = None
        product.deleted_on =  None
        
        try:
            validateObj = ProductsModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if ProductsModel.find_by_name(data['product_name']):
                return {"success": False, "message": "A product with that Record Name already exists"}, 400
            name=data['product_name']
            if name.strip():
                product.save_to_db()
                product.token = encodeID(product.product_id)
                product.save_to_db()
            else:
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return product.json(), 201