from flasgger import swag_from
from flask import request
from flask_restful import Resource, reqparse
from models.proveedor import ProveedorModel
from utils import paginated_results, restrict

class ProveedorResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nombre', type=str, required=True, help="Este campo no puede estar vacío")
    parser.add_argument('direccion', type=str)
    parser.add_argument('telefono', type=str)

    @swag_from('../swagger/proveedor/get_proveedor.yaml')
    def get(self, id):
        proveedor = ProveedorModel.find_by_id(id)
        if proveedor:
            return proveedor.json()
        return {'message': 'Proveedor no encontrado'}, 404

    @swag_from('../swagger/proveedor/put_proveedor.yaml')
    def put(self, id):
        data = ProveedorResource.parser.parse_args()
        proveedor = ProveedorModel.find_by_id(id)
        if proveedor:
            proveedor.nombre = data['nombre']
            proveedor.direccion = data.get('direccion')
            proveedor.telefono = data.get('telefono')
        else:
            return {'message': 'Proveedor no encontrado'}, 404
        
        try:
            proveedor.save_to_db()
        except Exception as e:
            return {"message": "Ocurrió un error al intentar guardar el proveedor en la base de datos."}, 500
        return proveedor.json()

    @swag_from('../swagger/proveedor/delete_proveedor.yaml')
    def delete(self, id):
        proveedor = ProveedorModel.find_by_id(id)
        if proveedor:
            proveedor.delete_from_db()
            return {'message': 'Proveedor eliminado'}
        return {'message': 'Proveedor no encontrado'}, 404


class ProveedorList(Resource):

    @swag_from('../swagger/proveedor/post_proveedor.yaml')
    def post(self):
        data = ProveedorResource.parser.parse_args()
        proveedor = ProveedorModel(
            nombre=data['nombre'], 
            direccion=data.get('direccion'),
            telefono=data.get('telefono')
        )
        try:
            proveedor.save_to_db()
        except Exception as e:
            return {"message": "Ocurrió un error al intentar guardar el proveedor en la base de datos."}, 500
        return proveedor.json(), 201
    
    @swag_from('../swagger/proveedor/get_proveedor_list.yaml')
    def get(self):
        proveedores = ProveedorModel.find_all()
        return {'proveedores': [proveedor.json() for proveedor in proveedores]}


class ProveedorSearch(Resource):
    @swag_from('../swagger/proveedor/search_proveedor.yaml')
    def post(self):
        query = ProveedorModel.query
        if request.json:
            filtros = request.json
            query = restrict(query, filtros, 'id', lambda x: ProveedorModel.id == x)
            query = restrict(query, filtros, 'nombre', lambda x: ProveedorModel.nombre.contains(x))
            query = restrict(query, filtros, 'direccion', lambda x: ProveedorModel.direccion.contains(x))
        return paginated_results(query)
