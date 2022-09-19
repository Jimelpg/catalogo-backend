from flask_restful import Resource, reqparse
from models.categoria import CategoriaModel
from flasgger import swag_from
from utils import paginated_results,restrict
from flask import request

class CategoriaList (Resource):
   ## @swag_from('../swagger/task/list_task.yaml')
    def get (self):
        query = CategoriaModel.query
        return paginated_results(query)

   