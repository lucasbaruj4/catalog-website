from flask_restful.reqparse import Namespace
from flask import request

# Función utilitaria para asignar un valor a un objeto solo si el valor no es None
def _assign_if_something(obj: object, newdata: Namespace, key: str):
    value = newdata.get(key)
    if value is not None:
        obj.__setattr__(key, value)

# Función para manejar la paginación de resultados
def paginated_results(query):
    pagination = request.args.get('pagination', 'true', str)
    jsondepth = request.args.get('jsondepth', 1, int)
    if pagination == 'true':
        paginated = query.paginate(page=request.args.get('page', 1, int))
        return {
            'page': paginated.page,
            'pages': paginated.pages,
            'items': [x.json(jsondepth) if jsondepth else x.json() for x in paginated.items]
        }
    else:
        return [x.json(jsondepth) if jsondepth else x.json() for x in query.all()]

# Función para aplicar filtros a las consultas
def restrict(query, filters, name, condition, null_condition=None):
    f = filters.get(name)
    if f is not None:
        if isinstance(f, str):
            if f != '':
                query = query.filter(condition(f))
        else:
            query = query.filter(condition(f))
    elif name is not None and null_condition is not None:
        query = query.filter(null_condition(name))
    return query
#mas funciones
def restrict(query, filtros, key, condition):
    if key in filtros:
        query = query.filter(condition(filtros[key]))
    return query

def paginated_results(query):
    results = query.all()  # Esto puede cambiar si necesitas paginar
    return [result.json() for result in results]
