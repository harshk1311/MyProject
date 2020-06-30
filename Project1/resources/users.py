from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.users import UsersModel
from datetime import datetime



class Users(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('user_type_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('company_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('phone',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('owner_manager',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('yearly_budget',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )



    parser.add_argument('logo',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('city',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('country_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('timezone',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('level',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('permission',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('assigned_brands',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('assigned_products',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('assigned_services',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('parent_user_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    
    def get(self, email):
        user = UsersModel.find_by_Email(email)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404

    def post(self, email):
        if UsersModel.find_by_Email(email):
            return {'message': "An user with email '{}' already exists.".format(email)}, 400

        data = self.parser.parse_args()

        user = UsersModel(email, **data)

        try:
            user.created_by=1
            user.created_on = datetime.now()
            user.modified_by = 0
            user.deleted_by = 0
            user.save_to_db()

        except:
            return {"message": "An error occurred while inserting the user."}, 500

        return user.json(), 201

    
    def delete(self, email):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        user = UsersModel.find_by_Email(email)
        if user:
            user.deleted_by =1
            user.deleted_on = datetime.now()
            user.save_to_db()
            #user.delete_from_db()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404

    def put(self, email):
        data = self.parser.parse_args()

        user = UsersModel.find_by_Email(email)

        if user:
            user.modified_on = datetime.now()
            user.modified_by = 1
            user.password = data['password']
            user.user_type_id = data['user_type_id']
            user.company_name = data['company_name']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.phone = data['phone']
            user.title = data['title']
            user.owner_manager = data['owner_manager']
            user.yearly_budget = data['yearly_budget']
            user.logo = data['logo']
            user.city = data['city']
            user.country_id = data['country_id']
            user.address = data['address']
            user.timezone = data['timezone']
            user.level = data['level']
            user.permission = data['permission']
            user.assigned_brands = data['assigned_brands']
            user.assigned_products = data['assigned_products']
            user.assigned_services = data['assigned_services']
            user.parent_user_id = data['parent_user_id']
            user.save_to_db()
            return user.json()
        else:
            return {'message': 'User not found.'}, 404