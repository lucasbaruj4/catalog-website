import os
import logging
from flask import Flask, redirect, request
from flasgger import Swagger
from flask_restful import Api
from resources.album import AlbumResource, AlbumList, AlbumSearch
from resources.artista import ArtistaList, ArtistaResource, ArtistaSearch
from resources.categoria import CategoriaResource, CategoriaList, CategoriaSearch
from resources.musica import MusicaList, MusicaResource, MusicaSearch
from resources.proveedor import ProveedorResource, ProveedorList, ProveedorSearch
from db import db
from flask_cors import CORS

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/api/*": {"origins": "*"}})
# Configuración de la API con manejo de errores
api = Api(
    app,
    errors={
        "NoAuthorizationError": {
            "message": "Request does not contain an access token.",
            "error": "authorization_required",
            "status": 401,
        }
    },
)

PREFIX = os.environ.get("PREFIX_PATH", "/api")

def env_config(name, default):
    app.config[name] = os.environ.get(name, default=default)

# Configuración de la base de datos
env_config(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql://postgres:postgres@localhost:5432/musica",
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["SQLALCHEMY_ECHO"] = False

# Configuración de Swagger
app.config["SWAGGER"] = {
    "title": "musica-backend",
    "version": "1.0.0",
    "description": "API de catálogo de música en Flask",
    "uiversion": 2,
    "tags": [{"name": "music"}],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": f"{PREFIX}/apispec_1.json",
            "rule_filter": lambda rule: True,  # Incluir todas las rutas
            "model_filter": lambda tag: True,  # Incluir todos los modelos
        }
    ],
    "specs_route": f"{PREFIX}/apidocs/",
    "static_url_path": f"{PREFIX}/static",
}

swagger = Swagger(app)
app.logger.setLevel(logging.INFO)

@app.route("/")
@app.route(f"{PREFIX}")
def welcome():
    return redirect(f"{PREFIX}/apidocs", code=302)
@app.route('/api/albums/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def handle_album(id):
    if request.method == 'OPTIONS':
        return '', 200
@app.route('/api/artistas/<int:id>', methods=['OPTIONS'])
def artista_options(id):
    return '', 200

# Registro de recursos en la API
api.add_resource(AlbumResource, "/api/albums/<id>")
api.add_resource(AlbumList, f"{PREFIX}/albums")
api.add_resource(AlbumSearch, f"{PREFIX}/search/albums")

api.add_resource(CategoriaResource, f"{PREFIX}/categoria/<id>")
api.add_resource(CategoriaList, f"{PREFIX}/categorias")
api.add_resource(CategoriaSearch, f"{PREFIX}/search/categorias")

# api.add_resource(ProveedorResource, f"{PREFIX}/proveedor/<id>")
# api.add_resource(ProveedorList, f"{PREFIX}/proveedores")
api.add_resource(ProveedorSearch, f"{PREFIX}/search/proveedores")

api.add_resource(ProveedorResource, '/api/proveedores/<int:id>')
api.add_resource(ProveedorList, '/api/proveedores')

# Registrar rutas
api.add_resource(ArtistaResource, '/api/artistas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
api.add_resource(ArtistaList, '/api/artistas', methods=['GET', 'POST'])
api.add_resource(ArtistaSearch, '/api/artistas/search', methods=['POST'])


api.add_resource(MusicaList, '/api/musicas')
api.add_resource(MusicaResource, '/api/musicas/<int:id>')
api.add_resource(MusicaSearch, '/api/musicas/search')






if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
else:
    db.init_app(app)
