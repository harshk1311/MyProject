from flask_restful import Resource,reqparse
from models.brandcategory import BrandCategoryModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class BrandCategory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('category_name',
                        type=str,
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

    @classmethod
    def get(cls, token):
        try:
            category_id = decodeID(token)
            category = BrandCategoryModel.find_by_id(category_id)
            if not category or category.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return category.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            category_id = decodeID(token)
            category = BrandCategoryModel.find_by_id(category_id)
            if not category or category.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            category.deleted_by =1
            category.deleted_on = datetime.now()
            category.save_to_db()
            #category.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = BrandCategoryModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            category_id = decodeID(token)
            category = BrandCategoryModel.find_by_id(category_id)
            if not category or category.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            category.category_name = data['category_name']
            category.modified_on = datetime.now()
            category.modified_by = 1
            category.logo = data['logo']
            name=data['category_name']
            if name.strip():
                category.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class BrandCategoryPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('category_name',
                        type=str,
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

    def post(self):
        data = self.parser.parse_args()
        category = BrandCategoryModel(**data)
        category.created_by = 1
        category.created_on = datetime.now()
        category.modified_by = 0
        category.deleted_by = 0
        category.modified_on = None
        category.deleted_on =  None
        
        try:
            validateObj = BrandCategoryModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if BrandCategoryModel.find_by_name(data['category_name']):
                return {"success": False, "message": "A category with that Record Name already exists"}, 400
            name=data['category_name']
            if name.strip():
                category.save_to_db()
                category.token = encodeID(category.category_id)
                category.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return category.json(), 201