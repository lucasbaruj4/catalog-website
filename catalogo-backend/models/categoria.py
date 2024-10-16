from db import BaseModel, db

class CategoriaModel(BaseModel):
    __tablename__ = 'categoria'
    id = db.Column(db.BigInteger, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)
    nombre = db.Column(db.String, nullable=False)

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def json(self, jsondepth=0):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'nombre': self.nombre
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
