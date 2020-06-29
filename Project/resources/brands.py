from flask_restful import Resource,reqparse
from models.brands import BrandsModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime

class Brands(Resource):
    parser = reqparse.RequestParser()
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

    def get(self, brand_name):
        brand = BrandsModel.find_by_name(brand_name)
        try :
            if brand:
                return brand.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    def put(self, brand_name):
        data = self.parser.parse_args()
        brand=BrandsModel.find_by_name(brand_name)
        if brand:
            brand.modified_on = datetime.now()
            brand.modified_by = 1
            brand.user_id = data['user_id']
            brand.industry_id = data['industry_id']
            brand.brand_category_id =data['brand_category_id']
            brand.save_to_db()
            
        else :
            return {"Message":"Record Not FOUND"}
        return brand.json()
    @classmethod
    def delete(cls, brand_name):
        brand = BrandsModel.find_by_name(brand_name)
        if brand:
            brand.deleted_by =1
            brand.deleted_on = datetime.now()
            brand.save_to_db()
            #brand.delete_from_db()
            return {'message': 'Record deleted'}
            
            
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, brand_name):
        db.create_all()
        db.session.commit()
        if BrandsModel.find_by_name(brand_name):
            return {'message': "An Record with name '{}' already exists.".format(brand_name)}, 400

        data = self.parser.parse_args()
        
        
        brand = BrandsModel(brand_name,**data,)
        brand.created_by = 1
        brand.created_on = datetime.now()
        brand.modified_by = 0
        brand.deleted_by = 0
        try:
            brand.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
            
        return brand.json(), 201
    