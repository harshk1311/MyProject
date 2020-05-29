from flask_restful import Resource
from models.Category import CategoryModel


class Category(Resource) :
    @classmethod
    def get(cls,cname):
        category=CategoryModel.find_by_name(cname)
        if category :
            return category.json()
        return {'message': 'Category not found'}, 404
        
    @classmethod
    def post(cls,cname):
        if CategoryModel.find_by_name(cname):
            return{'message': "A Category with name '{}' already exists.".format(cname)},400
        category =CategoryModel(cname)
        try:
            category.save_to_db()
        except:
            return {"message": "An error occurred creating the Category."}, 500

        return category.json(), 201

    @classmethod
    def delete(cls, cname):
        category = CategoryModel.find_by_name(cname)
        if category:
            category.delete_from_db()

        return {'message': 'Category deleted'}


class CatList(Resource):
    @classmethod
    def get(cls):
        return {'stores': [category.json() for category in CategoryModel.find_all()]}
