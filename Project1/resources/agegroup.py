from flask_restful import Resource,reqparse
from models.agegroup import AgeGroupModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class AgeGroup(Resource):
    
    def get(self, age_group):
        age_group = AgeGroupModel.find_by_name(age_group)
        try :
            if age_group:
                return age_group.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    
    @classmethod
    def delete(cls, age_group):
        age_group = AgeGroupModel.find_by_name(age_group)
        if age_group:
            age_group.deleted_by =1
            age_group.deleted_on = datetime.now()
            age_group.save_to_db()
            #age_group.delete_from_db()
            return {'message': 'Record deleted'}
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, age_group):
        db.create_all()
        db.session.commit()
        if AgeGroupModel.find_by_name(age_group):
            return {'message': "An Record with name '{}' already exists.".format(age_group)}, 400
        age_group = AgeGroupModel(age_group)
        age_group.created_by = 1
        age_group.created_on = datetime.now()
        age_group.modified_by = 0
        age_group.deleted_by = 0
        try:
            age_group.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
            
        return age_group.json(), 201