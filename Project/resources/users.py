from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.users import UsersModel
from datetime import datetime



class Users(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Password',
                        type=str,
                        required=True,
                        help="Please Enter Password!!!!...."
                        )

    @jwt_required
    def get(self, Email):
        user = UsersModel.find_by_Email(Email)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404

    def post(self, Email):
        if UsersModel.find_by_Email(Email):
            return {'message': "An user with Email '{}' already exists.".format(Email)}, 400

        data = self.parser.parse_args()

        user = UsersModel(Email, **data)

        try:
            user.CreatedOn = datetime.utcnow()
            user.save_to_db()

        except:
            return {"message": "An error occurred while inserting the user."}, 500

        return user.json(), 201

    @jwt_required
    def delete(self, Email):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        user = UsersModel.find_by_Email(Email)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404

    def put(self, Email):
        data = self.parser.parse_args()

        user = UsersModel.find_by_Email(Email)

        if user:
            user = UsersModel(Email, **data)
            user.save_to_db()
            return user.json()
        else:
            return {'message': 'User not found.'}, 404