from flasgger import swag_from
from flask import request
from flask_restful import Resource, reqparse
from models.album import AlbumModel
from models.album import AlbumModel
from utils import restrict, paginated_results
from flasgger import swag_from


class AlbumResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nombre', type=str, required=True, help="Este campo no puede estar vacío")
    parser.add_argument('descripcion', type=str)
    parser.add_argument('proveedor_id', type=int, required=True, help="Este campo no puede estar vacío")
    parser.add_argument('categoria_id', type=int, required=True, help="Este campo no puede estar vacío")
    parser.add_argument('artista_id', type=int, required=True, help="Este campo no puede estar vacío")
    parser.add_argument('precio', type=float, required=True, help="Este campo no puede estar vacío")
    parser.add_argument('estado', type=bool, required=True, help="Este campo no puede estar vacío")

    @swag_from('../swagger/album/get_album.yaml')
    def get(self, id):
        album = AlbumModel.find_by_id(id)
        if album:
            return album.json()
        return {'message': 'Album no encontrado'}, 404

    
    @swag_from('../swagger/album/put_album.yaml')
    def put(self, id):
        data = AlbumResource.parser.parse_args()

        # Buscamos el álbum por ID
        album = AlbumModel.find_by_id(id)

        if album:
            # Actualizamos los valores del álbum si los datos son proporcionados
            album.nombre = data['nombre']
            album.descripcion = data['descripcion'] if data['descripcion'] is not None else album.descripcion
            album.proveedor_id = data['proveedor_id'] if data['proveedor_id'] is not None else album.proveedor_id
            album.categoria_id = data['categoria_id'] if data['categoria_id'] is not None else album.categoria_id
            album.artista_id = data['artista_id'] if data['artista_id'] is not None else album.artista_id
            album.precio = data['precio'] if data['precio'] is not None else album.precio
            album.estado = data['estado'] if data['estado'] is not None else album.estado

            try:
                album.save_to_db()
                return album.json(), 200  # Asegúrate de devolver una respuesta válida con un código de estado
            except Exception as e:
                return {"message": "Ocurrió un error al intentar actualizar el álbum en la base de datos."}, 500

        return {'message': 'Álbum no encontrado'}, 404  # Si el álbum no se encuentra, devolvemos un 404



    @swag_from('../swagger/album/delete_album.yaml')
    def delete(self, id):
        album = AlbumModel.find_by_id(id)
        if album:
            album.delete_from_db()
            return {'message': 'Album eliminado'}
        return {'message': 'Album no encontrado'}, 404


class AlbumList(Resource):
    
    @swag_from('../swagger/album/post_album.yaml')
    def post(self):
        data = AlbumResource.parser.parse_args()
        album = AlbumModel(
        nombre=data['nombre'], 
        descripcion=data.get('descripcion'), 
        proveedor_id=data['proveedor_id'],
        categoria_id=data['categoria_id'],
        artista_id=data['artista_id'],
        precio=data['precio'],
        estado=data['estado']
    ) 
        try:
            album.save_to_db()
        except Exception as e:
            return {"message": "Ocurrió un error al intentar guardar el álbum en la base de datos."}, 500
        return album.json(), 201

    @swag_from('../swagger/album/get_album_list.yaml')  
    def get(self):
        albums = AlbumModel.find_all()
        return {'albums': [album.json() for album in albums]}

class AlbumSearch(Resource):
    @swag_from('../swagger/album/search_album.yaml')
    def post(self):
        query = AlbumModel.query
        if request.json:
            filtros = request.json
            query = restrict(query, filtros, 'id', lambda x: AlbumModel.id == x)
            query = restrict(query, filtros, 'nombre', lambda x: AlbumModel.nombre.contains(x))
        return paginated_results(query)
