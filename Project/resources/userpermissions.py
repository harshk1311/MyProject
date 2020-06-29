from flask_restful import Resource,reqparse
from models.userpermissions import UserPermissionModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class UserPermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('feature_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('user_type_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    

    def get(self, section_name):
        userpermission = UserPermissionModel.find_by_name(section_name)
        try :
            if userpermission:
                return userpermission.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    def put(self, section_name):
        data = self.parser.parse_args()
        userpermission=UserPermissionModel.find_by_name(section_name)
        if userpermission:
            userpermission.modified_on = datetime.now()
            userpermission.modified_by = 1
            userpermission.feature_name = data['feature_name']
            userpermission.user_type_id = data['user_type_id']

            userpermission.save_to_db()
            
        else :
            return {"Message":"Record Not FOUND"}
        return userpermission.json()
    @classmethod
    def delete(cls, section_name):
        userpermission = UserPermissionModel.find_by_name(section_name)
        if userpermission:
            userpermission.deleted_by =1
            userpermission.deleted_on = datetime.now()
            userpermission.save_to_db()
            userpermission.delete_from_db()
            return {'message': 'Record deleted'}
            
            
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, section_name):
        db.create_all()
        db.session.commit()
        if UserPermissionModel.find_by_name(section_name):
            return {'message': "An Record with name '{}' already exists.".format(section_name)}, 400

        data = self.parser.parse_args()
        
        
        userpermission = UserPermissionModel(section_name,**data,)
        userpermission.created_by = 1
        userpermission.created_on = datetime.now()
        userpermission.modified_by = 0
        userpermission.deleted_by = 0
        try:
            validate(data,check)
            userpermission.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
            
        return userpermission.json(), 201