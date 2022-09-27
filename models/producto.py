#asi se define una clase en python ej "class nombre_clase"
#agregarle atributos y de que tipo es
#self es como el objeto del this
from collections import UserList
from db import db
from flask_restful.reqparse import Namespace
from utils import _assign_if_something
from models.proveedor import ProveedorModel
from models.categoria import CategoriaModel

class ProductoModel(db.Model):
    __tablename__ = 'producto'

    id = db.Column(db.Integer, primary_key = True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey(ProveedorModel.id))
    categoria_id = db.Column(db.Integer, db.ForeignKey(CategoriaModel.id))
    nombre = db.Column(db.String)
    descrip = db.Column(db.String)
    precio = db.Column(db.Integer)
    estado = db.Column(db.String)

    _proveedor = db.relationship('ProveedorModel', 
    uselist = False, 
    primaryjoin='ProveedorModel.id == ProductoModel.proveedor_id', 
    foreign_keys='ProductoModel.proveedor_id')

    _categoria = db.relationship('CategoriaModel', 
    uselist = False, 
    primaryjoin='CategoriaModel.id == ProductoModel.categoria_id', 
    foreign_keys='ProductoModel.categoria_id')

#se van a setear según los parametros asignados que se llaman igual 
    def __init__(self, id, proveedor_id, categoria_id, nombre, descrip, precio, estado):
        self.id = id
        self.proveedor_id = proveedor_id
        self.categoria_id = categoria_id
        self.nombre = nombre
        self.descrip = descrip
        self.precio = precio
        self.estado = estado

#metodo para retomar el objeto en formato json o diccionario
    def json(self, depth =0):
        json = {
            'id': self.id,
            'proveedor_id': self.proveedor_id,
            'categoria_id': self.categoria_id,
            'nombre': self.nombre,
            'descrip': self.descrip,
            'precio': self.precio,
            'estado': self.estado
        }
        if depth >0:
            if self._proveedor:
                json['_proveedor'] = self._proveedor.json(depth)
            if self._categoria:
                json['_categoria'] = self._categoria.json(depth)

        return json

 #saber de memoria // @ indica que este metodo es un metodo de la clase que sera utilizado en otro lugar 
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    #comparacuion campo por campo
    def from_reqparse(self, newdata: Namespace):
        for no_pk_key in ['proveedor_id', 'categoria_id', 'nombre', 'descrip', 'precio', 'estado' ]:
            _assign_if_something(self, newdata, no_pk_key)

#tarea.id=1
#tarea.descrip = "Hola Jimena"
#tarea.json()
#{'id':1, 'descrip': "Hola Jimena"}




    