from flask import Flask, jsonify,render_template,request
from flask_restful import Api
from flask_jwt_extended import JWTManager


from blacklist import BLACKLIST
from resources.users import Users,UsersModel
from resources.industry import Industry,IndustryModel
from resources.brands import Brands,BrandsModel
from resources.userpermissions import UserPermission,UserPermissionModel
from resources.userlevel import UserLevel,UserLevelModel
from resources.brandcategory import BrandCategory,BrandCategoryModel
from resources.products import Products,ProductsModel
from resources.service import Service,ServiceModel
#
from resources.agegroup import AgeGroup,AgeGroupModel
from resources.gender import Gender,GenderModel
from resources.language import Language,LanguageModel
from resources.nationality import Nationality,NationalityModel
from resources.education import Education,EducationModel
from resources.occupation import Occupation,OccupationModel
from resources.target_audience_profile import TargetAudienceProfile,TargetAudienceProfileModel
from resources.campaign import Campaign,CampaignModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:oracle@localhost/project_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

"""
JWT related configuration. The following functions includes:
1) add claims to each jwt
2) customize the token expired error message 
"""
app.config['JWT_SECRET_KEY'] = 'jose'  # we can also use app.secret like before, Flask-JWT-Extended can recognize both
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
jwt = JWTManager(app)

"""
`claims` are data we choose to attach to each jwt payload
and for each jwt protected endpoint, we can retrieve these claims via `get_jwt_claims()`
one possible use case for claims are access level control, which is shown below
"""
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # instead of hard-coding, we should read from a config file to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
       'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401

# JWT configuration ends


@app.before_first_request
def create_tables():
    db.create_all()



@app.route('/login',methods=['GET']) 
def login():
    return render_template('login.html')
   
api.add_resource(Users, '/user/<string:email>')
api.add_resource(Industry, '/industry/<string:industry_name>')
api.add_resource(Brands,'/brand/<string:brand_name>')
api.add_resource(UserPermission,'/userpermission/<string:section_name>')
api.add_resource(UserLevel,'/userlevel/<string:level_name>')
api.add_resource(BrandCategory,'/brandcategory/<string:category_name>')
api.add_resource(Products,'/product/<string:product_name>')
api.add_resource(Service,'/service/<string:service_name>')
api.add_resource(AgeGroup,'/agegroup/<string:age_group>')
api.add_resource(Gender,'/gender/<string:gender_name>')
api.add_resource(Language,'/language/<string:language_name>')
api.add_resource(Nationality,'/nationality/<string:nationality_name>')
api.add_resource(Education,'/education/<string:education_name>')
api.add_resource(Occupation,'/occupation/<string:occupation_name>')
api.add_resource(TargetAudienceProfile,'/audience/<string:audience_profile_name>')
api.add_resource(Campaign,'/campaign/<string:campaign_name>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
