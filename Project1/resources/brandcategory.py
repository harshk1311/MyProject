from flask_restful import Resource,reqparse
from models.brandcategory import BrandCategoryModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class BrandCategory(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('logo',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    

    def get(self, category_name):
        brandcategory = BrandCategoryModel.find_by_name(category_name)
        try :
            if brandcategory:
                return brandcategory.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404


    def put(self, category_name):
        data = self.parser.parse_args()
        brandcategory=BrandCategoryModel.find_by_name(category_name)
        if brandcategory:
            brandcategory.modified_on = datetime.now()
            brandcategory.modified_by = 1
            brandcategory.logo = data['logo']
            brandcategory.save_to_db()
        else :
            return {"Message":"Record Not FOUND"}
        return brandcategory.json()

    @classmethod
    def delete(cls, category_name):
        brandcategory = BrandCategoryModel.find_by_name(category_name)
        if brandcategory:
            brandcategory.deleted_by =1
            brandcategory.deleted_on = datetime.now()
            brandcategory.save_to_db()
            
            return {'message': 'Record deleted'}
            
            
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, category_name):

        db.create_all()
        db.session.commit()
        if BrandCategoryModel.find_by_name(category_name):
            return {'message': "An Record with name '{}' already exists.".format(category_name)}, 400

        data = self.parser.parse_args()
        
        
        brandcategory = BrandCategoryModel(category_name,**data,)
        brandcategory.created_by = 1
        brandcategory.created_on = datetime.now()
        brandcategory.modified_by = 0
        brandcategory.deleted_by = 0
        try:
            brandcategory.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
            
        return brandcategory.json(), 201