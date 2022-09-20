from flask_restful import Resource, reqparse
from models.proveedor import ProveedorModel
from flasgger import swag_from
from utils import paginated_results,restrict
from flask import request

class ProveedorList (Resource):
    @swag_from('../swagger/proveedor/list_proveedor.yaml')
    def get (self):
        query = ProveedorModel.query
        return paginated_results(query)