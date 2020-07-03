from flask_restful import Resource,reqparse
from models.campaign import CampaignModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db
from flask import request
from datetime import datetime
from utilities import *
class Campaign(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('campaign_name',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('description',
                        type=str,
                        required=True,
                        trim=True,
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
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('exclude_locations',
                        type=str,
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    @classmethod
    def get(cls, token):
        try:
            campaign_id = decodeID(token)
            campaign = CampaignModel.find_by_id(campaign_id)
            if not campaign or campaign.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            return campaign.json(), 200
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @classmethod
    def delete(cls, token):
        try:
            campaign_id = decodeID(token)
            campaign = CampaignModel.find_by_id(campaign_id)
            if not campaign or campaign.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
            campaign.deleted_by =1
            campaign.deleted_on = datetime.now()
            campaign.save_to_db()
            #campaign.delete_from_db()
            return {"success": True, 'message': 'Record deleted.'}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}


    
    def put(self, token):
        try:
            data = self.parser.parse_args()
            validateObj = CampaignModel.validateData(data, request)
            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400
            
            campaign_id = decodeID(token)
            campaign = CampaignModel.find_by_id(campaign_id)
            if not campaign or campaign.token != token:
                return {"success": False, 'message': 'Record Not Found'}, 404
            
                
            campaign.category_name = data['campaign_name']
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
            campaign.modified_on = datetime.now()
            campaign.modified_by = 1
            ########
            campaign_name = data['campaign_name']
            description = data['description']
            target_locations = data['target_locations']
            exclude_locations = data['exclude_locations']
            if (campaign_name.strip() and description.strip() and target_locations.strip() and exclude_locations.strip()):
                campaign.save_to_db()
            else :
                return {"success": False, "message":"String Should not be empty"}
            
            return {"success": True, "message": "Record updated successfully."}, 200
        except Exception as e:
            return {"success": False, "message": str(e)}
class CampaignPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('campaign_name',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('description',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('brand_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('product_ids',
                        
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
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('exclude_locations',
                        
                        required=True,
                        trim=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = self.parser.parse_args()
        campaign = CampaignModel(**data)
        campaign.created_by = 1
        campaign.created_on = datetime.now()
        campaign.modified_by = 0
        campaign.deleted_by = 0
        campaign.modified_on = None
        campaign.deleted_on =  None
        
        try:
            validateObj = CampaignModel.validateData(data, request)

            if type(validateObj) is dict:
                return {"success": False, "errors": validateObj}, 400

            if CampaignModel.find_by_name(data['campaign_name']):
                return {"success": False, "message": "A campaign with that Record Name already exists"}, 400
            campaign_name = data['campaign_name']
            description = data['description']
            target_locations = data['target_locations']
            exclude_locations = data['exclude_locations']
            ########################  CHECKING STRING HAS VALUE OR NOT###################################################
            if (campaign_name.strip() and description.strip() and target_locations.strip() and exclude_locations.strip()):
                campaign.save_to_db()
                campaign.token = encodeID(campaign.campaign_id)
                campaign.save_to_db()

            else:
                return {"success": False, "message":"String Should not be empty"}
            
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return campaign.json(), 201