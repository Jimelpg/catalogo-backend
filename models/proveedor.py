from db import db
from flask_restful.reqparse import Namespace
from utils import _assign_if_something

class ProveedorModel (db.Model):
    __tablename__ = 'proveedor'

    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String)
    direccion = db.Column(db.String)
    telefono = db.Column(db.String)

#se van a setear según los parametros asignados que se llaman igual 
    def __init__(self, id, nombre, direccion, telefono):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

#metodo para retomar el objeto en formato json o diccionario
    def json(self, depht =0):
        json = {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': self.telefono
        }

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
    #comparacion campo por campo
    def from_reqparse(self, newdata: Namespace):
        for no_pk_key in ['nombre', 'direccion', 'telefono']:
            _assign_if_something(self, newdata, no_pk_key)
