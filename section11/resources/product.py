from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.product import ProductModel




class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('cid',
                        type=int,
                        required=True,
                        help="Every product needs a Category_ID."
                        )

    @jwt_required
    def get(self, name):
        product = ProductModel.find_by_name(name)
        if product:
            return product.json()
        return {'message': 'product not found'}, 404

    @fresh_jwt_required
    def post(self, name):
        if ProductModel.find_by_name(name):
            return {'message': "An Product with name '{}' already exists.".format(name)}, 400

        data = self.parser.parse_args()

        product = ProductModel(name, **data)

        try:
            product.save_to_db()
        except:
            return {"message": "An error occurred while inserting the Product."}, 500

        return product.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        product = ProductModel.find_by_name(name)
        if product:
            product.delete_from_db()
            return {'message': 'Product deleted.'}
        return {'message': 'product not found.'}, 404

    def put(self, name):
        data = self.parser.parse_args()

        product = ProductModel.find_by_name(name)

        if product:
            product.price = data['price']
        else:
            product = ProductModel(name, **data)

        product.save_to_db()

        return product.json()


class ProductList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        product = [product.json() for product in ProductModel.find_all()]
        if user_id:
            return {'product': product}, 200
        return {
            'product': [product['name'] for product in product],
            'message': 'More data available if you log in.'
        }, 200
