from flask import request
from flask_restful import Resource, reqparse
from flasgger import swag_from
from models.musica import MusicaModel
from utils import paginated_results, restrict

class MusicaResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('album_id', type=int, required=True, help="This field cannot be left blank.")
    parser.add_argument('proveedor_id', type=int, required=True, help="This field cannot be left blank.")
    parser.add_argument('categoria_id', type=int, required=True, help="This field cannot be left blank.")
    parser.add_argument('artista_id', type=int, required=True, help="This field cannot be left blank.")
    parser.add_argument('nombre', type=str, required=True, help="This field cannot be left blank.")
    parser.add_argument('descripcion', type=str, required=True, help="This field cannot be left blank.")
    @swag_from('../swagger/musica/get_musica.yaml')
    def get(self, id):
        musica = MusicaModel.find_by_id(id)
        if musica:
            return musica.json()
        return {'message': 'Musica not found'}, 404

    
    @swag_from('../swagger/musica/delete_musica.yaml')
    def delete(self, id):
        musica = MusicaModel.find_by_id(id)
        if musica:
            musica.delete_from_db()
            return {'message': 'Musica deleted.'}
        return {'message': 'Musica not found.'}, 404

    @swag_from('../swagger/musica/put_musica.yaml')
    def put(self, id):
        data = MusicaResource.parser.parse_args()

        musica = MusicaModel.find_by_id(id)

        if musica:
            musica.album_id = data['album_id'] if data['album_id'] is not None else musica.album_id
            musica.proveedor_id = data['proveedor_id'] if data['proveedor_id'] is not None else musica.proveedor_id
            musica.categoria_id = data['categoria_id'] if data['categoria_id'] is not None else musica.categoria_id
            musica.artista_id = data['artista_id'] if data['artista_id'] is not None else musica.artista_id
            musica.nombre = data['nombre']
            musica.descripcion = data['descripcion'] if data['descripcion'] is not None else musica.descripcion
        else:
            musica = MusicaModel(id, **data)

        try:
            musica.save_to_db()
        except Exception as e:
            return {"message": "Ocurrió un error al intentar actualizar la música en la base de datos."}, 500

        return musica.json()


class MusicaList(Resource):
    
    @swag_from('../swagger/musica/post_musica.yaml')
    def post(self):
        data = MusicaResource.parser.parse_args()
        musica = MusicaModel(
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        album_id=data['album_id'],
        proveedor_id=data['proveedor_id'],
        categoria_id=data['categoria_id'],
        artista_id=data['artista_id']
            ) 
        try:
            musica.save_to_db()
        except:
            return {"message": "An error occurred inserting the musica."}, 500

        return musica.json(), 201

    @swag_from('../swagger/musica/get_musica_list.yaml')
    def get(self):
        return {'musicas': [musica.json() for musica in MusicaModel.find_all()]}

class MusicaSearch(Resource):
    @swag_from('../swagger/musica/search_musica.yaml')
    def post(self):
        query = MusicaModel.query
        if request.json:
            filtros = request.json
            query = restrict(query, filtros, 'id', lambda x: MusicaModel.id == x)
            query = restrict(query, filtros, 'nombre', lambda x: MusicaModel.nombre.contains(x))
            query = restrict(query, filtros, 'album_id', lambda x: MusicaModel.album_id == x)
            query = restrict(query, filtros, 'proveedor_id', lambda x: MusicaModel.proveedor_id == x)
            query = restrict(query, filtros, 'categoria_id', lambda x: MusicaModel.categoria_id == x)
            query = restrict(query, filtros, 'artista_id', lambda x: MusicaModel.artista_id == x)
        return paginated_results(query)