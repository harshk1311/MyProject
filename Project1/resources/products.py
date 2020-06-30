from flask_restful import Resource,reqparse
from models.products import ProductsModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class Products(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('logo',
                        type=str,
                        required=True,
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
    

    def get(self, product_name):
        product = ProductsModel.find_by_name(product_name)
        try :
            if product:
                return product.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    def put(self, product_name):
        data = self.parser.parse_args()
        product=ProductsModel.find_by_name(product_name)
        if product:
            product.modified_on = datetime.now()
            product.modified_by = 1
            product.logo = data['logo']
            product.brand_id = data['brand_id']
            product.category_id = data['category_id']
            
        else :
            return {"Message":"Record Not FOUND"}
        product.save_to_db()
        return product.json()
    @classmethod
    def delete(cls, product_name):
        product = ProductsModel.find_by_name(product_name)
        if product:
            product.deleted_by =1
            product.deleted_on = datetime.now()
            product.save_to_db()
            #product.delete_from_db()
            return {'message': 'Record deleted'}
            
            
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, product_name):
        db.create_all()
        db.session.commit()
        if ProductsModel.find_by_name(product_name):
            return {'message': "An Record with name '{}' already exists.".format(product_name)}, 400

        data = self.parser.parse_args()
        
        
        product = ProductsModel(product_name,**data,)
        product.created_by = 1
        product.created_on = datetime.now()
        product.modified_by = 0
        product.deleted_by = 0
        try:
            
            product.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
            
        return product.json(), 201