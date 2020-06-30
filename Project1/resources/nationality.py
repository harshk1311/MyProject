from flask_restful import Resource,reqparse
from models.nationality import NationalityModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class Nationality(Resource):
    
    def get(self, nationality_name):
        nationality = NationalityModel.find_by_name(nationality_name)
        try :
            if nationality:
                return nationality.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    
    @classmethod
    def delete(cls, nationality_name):
        nationality = NationalityModel.find_by_name(nationality_name)
        if nationality:
            nationality.deleted_by =1
            nationality.deleted_on = datetime.now()
            nationality.save_to_db()
            #nationality.delete_from_db()
            return {'message': 'Record deleted'}
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, nationality_name):
        db.create_all()
        db.session.commit()
        if NationalityModel.find_by_name(nationality_name):
            return {'message': "An Record with name '{}' already exists.".format(nationality_name)}, 400
        nationality = NationalityModel(nationality_name)
        nationality.created_by = 1
        nationality.created_on = datetime.now()
        nationality.modified_by = 0
        nationality.deleted_by = 0
        try:
            nationality.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
        return nationality.json(), 201