from flasgger import swag_from
from flask import request
from flask_restful import Resource, reqparse
from models.categoria import CategoriaModel
from utils import paginated_results, restrict

class CategoriaResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nombre', type=str, required=True, help="Este campo no puede estar vacío")
    parser.add_argument('descripcion', type=str, required=False)

  
    @swag_from('../swagger/categoria/get_categoria.yaml')
    def get(self, id):
        categoria = CategoriaModel.find_by_id(id)
        if categoria:
            return categoria.json()
        return {'message': 'Categoría no encontrada'}, 404

    @swag_from('../swagger/categoria/put_categoria.yaml')
    def put(self, id):
        data = CategoriaResource.parser.parse_args()
        categoria = CategoriaModel.find_by_id(id)
        if categoria:
            categoria.nombre = data['nombre']
            categoria.descripcion = data['descripcion']
        else:
            categoria = CategoriaModel(id=id, **data)
        
        try:
            categoria.save_to_db()
        except Exception as e:
            return {"message": "Ocurrió un error al intentar guardar la categoría en la base de datos."}, 500
        return categoria.json()

    @swag_from('../swagger/categoria/delete_categoria.yaml')
    def delete(self, id):
        categoria = CategoriaModel.find_by_id(id)
        if categoria:
            categoria.delete_from_db()
            return {'message': 'Categoría eliminada'}
        return {'message': 'Categoría no encontrada'}, 404


class CategoriaList(Resource):
    
    @swag_from('../swagger/categoria/post_categoria.yaml')
    def post(self):
        data = CategoriaResource.parser.parse_args()
        categoria = CategoriaModel(nombre=data['nombre'], descripcion=data.get('descripcion'))
        try:
            categoria.save_to_db()
        except Exception as e:
            return {"message": "Ocurrió un error al intentar guardar la categoría en la base de datos."}, 500
        return categoria.json(), 201
    
    @swag_from('../swagger/categoria/get_categoria_list.yaml')  # Asegúrate de crear este YAML si aún no lo tienes
    def get(self):
        categorias = CategoriaModel.find_all()
        return {'categorias': [categoria.json() for categoria in categorias]}


class CategoriaSearch(Resource):
    @swag_from('../swagger/categoria/search_categoria.yaml')
    def post(self):
        query = CategoriaModel.query
        if request.json:
            filtros = request.json
            query = restrict(query, filtros, 'id', lambda x: CategoriaModel.id == x)
            query = restrict(query, filtros, 'nombre', lambda x: CategoriaModel.nombre.contains(x))
            query = restrict(query, filtros, 'descripcion', lambda x: CategoriaModel.descripcion.contains(x))
        return paginated_results(query)
