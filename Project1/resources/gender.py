from flask_restful import Resource,reqparse
from models.gender import GenderModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class Gender(Resource):
    
    def get(self, gender_name):
        gender = GenderModel.find_by_name(gender_name)
        try :
            if gender:
                return gender.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    
    @classmethod
    def delete(cls, gender_name):
        gender = GenderModel.find_by_name(gender_name)
        if gender:
            gender.deleted_by =1
            gender.deleted_on = datetime.now()
            gender.save_to_db()
            #gender.delete_from_db()
            return {'message': 'Record deleted'}
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, gender_name):
        db.create_all()
        db.session.commit()
        if GenderModel.find_by_name(gender_name):
            return {'message': "An Record with name '{}' already exists.".format(gender_name)}, 400
        gender = GenderModel(gender_name)
        gender.created_by = 1
        gender.created_on = datetime.now()
        gender.modified_by = 0
        gender.deleted_by = 0
        try:
            gender.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
        return gender.json(), 201