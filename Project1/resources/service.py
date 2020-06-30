from flask_restful import Resource,reqparse
from models.service import ServiceModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class Service(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('logo',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('brand_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('category_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    

    def get(self, service_name):
        service = ServiceModel.find_by_name(service_name)
        try :
            if service:
                return service.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    def put(self, service_name):
        data = self.parser.parse_args()
        service=ServiceModel.find_by_name(service_name)
        if service:
            service.modified_on = datetime.now()
            service.modified_by = 1
            service.logo = data['logo']
            service.brand_id = data['brand_id']
            service.category_id = data['category_id']
            service.save_to_db()
            
        else :
            return {"Message":"Record Not FOUND"}
        return service.json()
    @classmethod
    def delete(cls, service_name):
        service = ServiceModel.find_by_name(service_name)
        if service:
            service.deleted_by =1
            service.deleted_on = datetime.now()
            service.save_to_db()
            #service.delete_from_db()
            return {'message': 'Record deleted'}
            
            
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, service_name):
        db.create_all()
        db.session.commit()
        if ServiceModel.find_by_name(service_name):
            return {'message': "An Record with name '{}' already exists.".format(service_name)}, 400

        data = self.parser.parse_args()
        service = ServiceModel(service_name,**data,)
        service.created_by = 1
        service.created_on = datetime.now()
        service.modified_by = 0
        service.deleted_by = 0
        try:
            service.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
            
        return service.json(), 201