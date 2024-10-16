from db import BaseModel, db
from models.categoria import CategoriaModel
from models.proveedor import ProveedorModel
from models.artista import ArtistaModel

class AlbumModel(BaseModel):  # Modelo de la base de datos para Album
    __tablename__ = 'album'
    id = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Boolean, default=True)
    categoria_id = db.Column(db.BigInteger, db.ForeignKey(CategoriaModel.id))
    proveedor_id = db.Column(db.BigInteger, db.ForeignKey(ProveedorModel.id))
    artista_id = db.Column(db.BigInteger, db.ForeignKey(ArtistaModel.id))

    # Relaciones
    categoria = db.relationship('CategoriaModel', uselist=False, primaryjoin='CategoriaModel.id == AlbumModel.categoria_id', foreign_keys='AlbumModel.categoria_id')
    proveedor = db.relationship('ProveedorModel', uselist=False, primaryjoin='ProveedorModel.id == AlbumModel.proveedor_id', foreign_keys='AlbumModel.proveedor_id')
    artista = db.relationship('ArtistaModel', uselist=False, primaryjoin='ArtistaModel.id == AlbumModel.artista_id', foreign_keys='AlbumModel.artista_id')

    def __init__(self, nombre, descripcion, precio, estado, categoria_id, proveedor_id, artista_id):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.estado = estado
        self.categoria_id = categoria_id
        self.proveedor_id = proveedor_id
        self.artista_id = artista_id

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': str(self.precio),
            'estado': self.estado,
            'categoria': self.categoria.nombre if self.categoria else None,
            'proveedor': self.proveedor.nombre if self.proveedor else None,
            'artista': self.artista.nombre if self.artista else None
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
