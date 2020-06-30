from flask_restful import Resource,reqparse
from models.occupation import OccupationModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class Occupation(Resource):
    
    def get(self, occupation_name):
        education = OccupationModel.find_by_name(occupation_name)
        try :
            if education:
                return education.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    
    @classmethod
    def delete(cls, occupation_name):
        education = OccupationModel.find_by_name(occupation_name)
        if education:
            education.deleted_by =1
            education.deleted_on = datetime.now()
            education.save_to_db()
            #education.delete_from_db()
            return {'message': 'Record deleted'}
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, occupation_name):
        db.create_all()
        db.session.commit()
        if OccupationModel.find_by_name(occupation_name):
            return {'message': "An Record with name '{}' already exists.".format(occupation_name)}, 400
        education = OccupationModel(occupation_name)
        education.created_by = 1
        education.created_on = datetime.now()
        education.modified_by = 0
        education.deleted_by = 0
        try:
            education.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
        return education.json(), 201