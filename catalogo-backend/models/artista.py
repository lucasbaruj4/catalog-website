from db import BaseModel, db

class ArtistaModel(BaseModel):
    __tablename__ = 'artista'
    id = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String)

    def __init__(self, nombre, descripcion=None):
        self.nombre = nombre
        self.descripcion = descripcion

    def json(self, jsondepth=0):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
