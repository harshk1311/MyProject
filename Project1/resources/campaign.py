from flask_restful import Resource,reqparse
from models.campaign import CampaignModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from datetime import datetime
import json
from jsonschema import validate

class Campaign(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('brand_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('product_ids',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('currency_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('budget_amount',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('objective_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('kpi_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('target_locations',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('exclude_locations',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def get(self, campaign_name):
        campaign = CampaignModel.find_by_name(campaign_name)
        try :
            if campaign:
                return campaign.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    def put(self, campaign_name):
        data = self.parser.parse_args()
        campaign=CampaignModel.find_by_name(campaign_name)
        if campaign:
            campaign.description = data['description']
            campaign.brand_id = data['brand_id']
            campaign.product_ids = data['product_ids']
            campaign.currency_id = data['currency_id']
            campaign.budget_amount = data['budget_amount']
            campaign.objective_id = data['objective_id']
            campaign.kpi_id = data['kpi_id']
            campaign.target_locations = data['target_locations']
            campaign.exclude_locations = data['exclude_locations']
            campaign.modified_on = datetime.now()
            campaign.modified_by = 1
        else :
            return {"Message":"Record Not FOUND"}
        campaign.save_to_db()
        return campaign.json()
    @classmethod
    def delete(cls, campaign_name):
        campaign = CampaignModel.find_by_name(campaign_name)
        if campaign:
            campaign.deleted_by =1
            campaign.deleted_on = datetime.now()
            campaign.save_to_db()
            #campaign.delete_from_db()
            return {'message': 'Record deleted'}
            
            
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, campaign_name):
        db.create_all()
        db.session.commit()
        if CampaignModel.find_by_name(campaign_name):
            return {'message': "An Record with name '{}' already exists.".format(campaign_name)}, 400

        data = self.parser.parse_args()
        
        campaign = CampaignModel(campaign_name,**data,)
        campaign.created_by = 1
        campaign.created_on = datetime.now()
        campaign.modified_by = 0
        campaign.deleted_by = 0
        campaign.start_date = datetime.now()
        campaign.end_date = datetime.now()
        campaign.days = 1
        try:
            
            campaign.save_to_db()
        except Exception as e:
            return {"message": "An error occurred while inserting the Record.'{}'".format(e)}
            
        return campaign.json(), 201