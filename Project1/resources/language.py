from flask_restful import Resource,reqparse
from models.language import LanguageModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class Language(Resource):
    
    def get(self, language_name):
        language = LanguageModel.find_by_name(language_name)
        try :
            if language:
                return language.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    
    @classmethod
    def delete(cls, language_name):
        language = LanguageModel.find_by_name(language_name)
        if language:
            language.deleted_by =1
            language.deleted_on = datetime.now()
            language.save_to_db()
            #language.delete_from_db()
            return {'message': 'Record deleted'}
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, language_name):
        db.create_all()
        db.session.commit()
        if LanguageModel.find_by_name(language_name):
            return {'message': "An Record with name '{}' already exists.".format(language_name)}, 400
        language = LanguageModel(language_name)
        language.created_by = 1
        language.created_on = datetime.now()
        language.modified_by = 0
        language.deleted_by = 0
        try:
            language.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
        return language.json(), 201