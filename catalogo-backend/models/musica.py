from db import BaseModel, db

class MusicaModel(BaseModel):
    __tablename__ = 'musica'
    
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    artista_id = db.Column(db.Integer, db.ForeignKey('artista.id'))
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255))  # Si tienes una columna de descripción

    album = db.relationship('AlbumModel', backref='musicas')
    proveedor = db.relationship('ProveedorModel', backref='musicas')
    categoria = db.relationship('CategoriaModel', backref='musicas')
    artista = db.relationship('ArtistaModel', backref='musicas')

    def __init__(self, album_id, proveedor_id, categoria_id, artista_id, nombre, descripcion=None):
        self.album_id = album_id
        self.proveedor_id = proveedor_id
        self.categoria_id = categoria_id
        self.artista_id = artista_id
        self.nombre = nombre
        self.descripcion = descripcion

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,  # Si tienes la columna de descripción
            'album': self.album.nombre if self.album else None,  # Accede al nombre del álbum relacionado
            'proveedor': self.proveedor.nombre if self.proveedor else None,  # Accede al nombre del proveedor relacionado
            'categoria': self.categoria.nombre if self.categoria else None,  # Accede al nombre de la categoría relacionada
            'artista': self.artista.nombre if self.artista else None  # Accede al nombre del artista relacionado
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
