from sqlalchemy_continuum import make_versioned
import sqlalchemy as sa
from flask_continuum import VersioningMixin
from db import db
from datetime import datetime

make_versioned(user_cls=None)


class CampaignModel(db.Model,VersioningMixin):
    __versioned__ = {}
    __tablename__ = 'campaign'

    campaign_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_name = db.Column(db.Unicode(255))
    description = db.Column(db.Unicode(255))
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.brand_id'))
    product_ids = db.Column(db.Unicode(255))
    currency_id = db.Column(db.Integer)
    budget_amount = db.Column(db.Integer)
    objective_id = db.Column(db.Integer)
    kpi_id = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    days = db.Column(db.Integer)
    target_locations = db.Column(db.Unicode(255))
    exclude_locations = db.Column(db.Unicode(255))


    created_by    = db.Column(db.Integer)
    created_on    = db.Column(db.DateTime)
    modified_by   = db.Column(db.Integer)
    modified_on   = db.Column(db.DateTime)
    deleted_by    = db.Column(db.Integer)
    deleted_on    = db.Column(db.DateTime)
    barnd        = db.relationship('BrandsModel')
    
    sa.orm.configure_mappers()

    def __init__(self,campaign_name,description,brand_id,product_ids,currency_id,budget_amount,objective_id,kpi_id,target_locations,exclude_locations):
        self.campaign_name = campaign_name
        self.description = description
        self.brand_id = brand_id 
        self.product_ids = product_ids
        self.currency_id = currency_id
        self.budget_amount = budget_amount
        self.objective_id = objective_id
        self.kpi_id = kpi_id
        self.target_locations = target_locations
        self.exclude_locations = exclude_locations
   

    def json(self):
        return{
            'id':self.campaign_id,
            'name':self.campaign_name,
        }
    @classmethod 
    def find_by_name(cls,campaign_name):
        return cls.query.filter_by(campaign_name=campaign_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()