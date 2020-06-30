from flask_restful import Resource,reqparse
from models.userlevel import UserLevelModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class UserLevel(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('user_type_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    

    def get(self, level_name):
        userlevel = UserLevelModel.find_by_name(level_name)
        try :
            if userlevel:
                return userlevel.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    def put(self, level_name):
        data = self.parser.parse_args()
        userlevel=UserLevelModel.find_by_name(level_name)
        if userlevel:
            userlevel.modified_on = datetime.now()
            userlevel.modified_by = 1
            userlevel.user_type_id = data['user_type_id']
            userlevel.save_to_db()
            
        else :
            return {"Message":"Record Not FOUND"}
        return userlevel.json()

    @classmethod
    def delete(cls, level_name):
        userlevel = UserLevelModel.find_by_name(level_name)
        if userlevel:
            userlevel.deleted_by =1
            userlevel.deleted_on = datetime.now()
            userlevel.save_to_db()
            
            return {'message': 'Record deleted'}
            
            
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, level_name):
        db.create_all()
        db.session.commit()
        if UserLevelModel.find_by_name(level_name):
            return {'message': "An Record with name '{}' already exists.".format(level_name)}, 400

        data = self.parser.parse_args()
        
        
        userlevel = UserLevelModel(level_name,**data,)
        userlevel.created_by = 1
        userlevel.created_on = datetime.now()
        userlevel.modified_by = 0
        userlevel.deleted_by = 0
        try:
            userlevel.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
            
        return userlevel.json(), 201