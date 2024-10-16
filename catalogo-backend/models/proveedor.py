from db import BaseModel, db

class ProveedorModel(BaseModel):
    __tablename__ = 'proveedor'
    id = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    direccion = db.Column(db.String)
    telefono = db.Column(db.String)

    def __init__(self, nombre, direccion=None, telefono=None):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

    def json(self, jsondepth=0):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': self.telefono
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
