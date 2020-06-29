from flask_restful import Resource,reqparse
from models.industry import IndustryModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime

class Industry(Resource):
    parser = reqparse.RequestParser()

    def get(self, industry_name):
        industry = IndustryModel.find_by_name(industry_name)
        try :
            if industry:
                return industry.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    
    @classmethod
    def delete(cls, industry_name):
        industry = IndustryModel.find_by_name(industry_name)
        if industry:
            industry.deleted_by =1
            industry.deleted_on = datetime.now()
            industry.save_to_db()
            #industry.delete_from_db()
            return {'message': 'Record deleted'}
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, industry_name):
        db.create_all()
        db.session.commit()
        
        industry = IndustryModel(industry_name)
        industry.created_by = 1
        industry.created_on = datetime.now()
        industry.modified_by = 0
        industry.deleted_by = 0
        industry.modified_on = None
        industry.deleted_on =  None
        try:
            industry.save_to_db()
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return industry.json(), 201