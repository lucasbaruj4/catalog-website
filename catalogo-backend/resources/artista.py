from flasgger import swag_from
from flask import request
from flask_restful import Resource, reqparse
from models.artista import ArtistaModel
from utils import paginated_results, restrict

class ArtistaResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('nombre', type=str)
    parser.add_argument('descripcion',type=str)
   
   
   
    @swag_from('../swagger/artista/get_artista.yaml')
    def get(self, id):
        artista = ArtistaModel.find_by_id(id)
        if artista:
            return artista.json()
        return {'message': 'Artista no encontrado'}, 404

    

    @swag_from('../swagger/artista/put_artista.yaml')
    def put(self, id):
        data = ArtistaResource.parser.parse_args()
        artista = ArtistaModel.find_by_id(id)
        if artista:
            artista.nombre = data['nombre']
            artista.descripcion = data.get('descripcion')
        else:
            artista = ArtistaModel(id=id, nombre=data['nombre'], descripcion=data.get('descripcion'))
        
        try:
            artista.save_to_db()
        except Exception as e:
            return {"message": "Ocurrió un error al intentar guardar el artista en la base de datos."}, 500
        return artista.json()

    @swag_from('../swagger/artista/delete_artista.yaml')
    def delete(self, id):
        artista = ArtistaModel.find_by_id(id)
        if artista:
            artista.delete_from_db()
            return {'message': 'Artista eliminado'}
        return {'message': 'Artista no encontrado'}, 404


class ArtistaList(Resource):

    @swag_from('../swagger/artista/post_artista.yaml')
    def post(self):
        data = ArtistaResource.parser.parse_args()
        artista = ArtistaModel(nombre=data['nombre'], descripcion=data.get('descripcion'))
        try:
            artista.save_to_db()
        except Exception as e:
            return {"message": "Ocurrió un error al intentar guardar el artista en la base de datos."}, 500
        return artista.json(), 201
    
    @swag_from('../swagger/artista/get_artista_list.yaml')  # Asegúrate de crear este YAML si aún no lo tienes
    def get(self):
        artistas = ArtistaModel.find_all()
        return {'artistas': [artista.json() for artista in artistas]}
    
    

class ArtistaSearch(Resource):
    @swag_from('../swagger/artista/search_artista.yaml')
    def post(self):
        query = ArtistaModel.query
        if request.json:
            filtros = request.json
            query = restrict(query, filtros, 'id', lambda x: ArtistaModel.id == x)
            query = restrict(query, filtros, 'nombre', lambda x: ArtistaModel.nombre.contains(x))
        return paginated_results(query)