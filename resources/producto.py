#crear un constructor = resources
# def es para definir metodos
# __int__ para definir constructores
#jason es para retornar el objeto en formao json = diccionario
# get me trae todos los datos por ejemplo con el id me trae los datos de la tarea
# 404  es el código de error
#401 no autorizado (mas ppt)

from pickletools import int4
from flask_restful import Resource, reqparse
from models.producto import ProductoModel
from flasgger import swag_from
from utils import paginated_results,restrict
from flask import request


class Producto (Resource):

    #para el manejo de peticiones
    #reqparse.RequestParse()

    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('proveedor_id', type= int)
    parser.add_argument('categoria_id', type= int)
    parser.add_argument('nombre', type= str)
    parser.add_argument('descrip', type= str)
    parser.add_argument('precio', type= int)
    parser.add_argument('estado', type= str)

    @swag_from('../swagger/producto/get_producto.yaml')
    def get(self, id):
        producto = ProductoModel.find_by_id(id)
        if producto:
            return producto.json()
        return {'message': "No se encuentra el producto"},404

    #para actualizar un registro ya existente
    @swag_from('../swagger/producto/put_producto.yaml')
    def put(self, id):
        producto = ProductoModel.find_by_id(id)
        if producto:
            newdata = producto.parser.parse_args()
            producto.from_reqparse(newdata)
            producto.save_to_db()
            return producto.json()
        

    @swag_from('../swagger/producto/delete_producto.yaml')
    def delete(self, id):
        producto = ProductoModel.find_by_id(id)
        if producto:
            producto.delete_from_db()

        return {'message': 'Se ha borrado el producto'}




class ProductoList (Resource):
    @swag_from('../swagger/producto/list_producto.yaml')
    def get (self):
        query = ProductoModel.query
        return paginated_results(query)

    @swag_from('../swagger/producto/post_producto.yaml')
    def post(self):
        data = Producto.parser.parse_args()

        producto = ProductoModel(**data) #para convertir un json en un objeto tarea

        try:
            producto.save_to_db()
        except Exception as e: #el try es para manejar los errores que puede haber
            print(e)
            return {'message': 'Ocurrio un error al subir el producto'}, 500
        
        return producto.json(), 201
        


class ProductoSearch(Resource):
    @swag_from('../swagger/producto/search_producto.yaml')
    def post(self):
        query = ProductoModel.query
        if request.json:
            filtros = request.json
            query = restrict(query,filtros, 'id', lambda x: ProductoModel.id == x)
            query = restrict(query,filtros, 'proveedor_id', lambda x: ProductoModel.descrip.contains(x))
            query = restrict(query,filtros, 'categoria_id', lambda x: ProductoModel.id == x)
            query = restrict(query,filtros, 'nombre', lambda x: ProductoModel.descrip.contains(x))
            query = restrict(query,filtros, 'descrip', lambda x: ProductoModel.id == x)
            query = restrict(query,filtros, 'precio', lambda x: ProductoModel.descrip.contains(x))
            query = restrict(query,filtros, 'estado', lambda x: ProductoModel.id == x)
            # logica de filtrado de datos
        return paginated_results(query)

