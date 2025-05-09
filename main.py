from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#___Configuración del servidor y base de datos___
usuario_bd = 'root'
password_bd = '10503'
servidor_bd = 'localhost'
puerto_bd = '3306'
nombre_bd = 'portal'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{usuario_bd}:{password_bd}@{servidor_bd}:{puerto_bd}/{nombre_bd}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#___Inicialización de extensiones___
db = SQLAlchemy(app)
ma = Marshmallow(app)

#___Modelo de datos___
class Categoria(db.Model):
    __tablename__ = "categoria"

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    imagen_url = db.Column(db.String(255)) 

    def __init__(self, nombre, descripcion, imagen_url):
        self.nombre = nombre
        self.descripcion = descripcion
        self.imagen_url = imagen_url

#___Esquema de serialización___
class CategoriaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        load_instance = True

categoria_schema = CategoriaSchema()
categorias_schema = CategoriaSchema(many=True)

#___Rutas CRUD API___
@app.route('/categoria', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

@app.route('/categoria/<id>', methods=['GET'])
def get_categoriaID(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)

@app.route('/categoria', methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    nombre = data['nombre']
    descripcion = data['descripcion']
    imagen_url = data['imagen_url']
    nueva_categoria = Categoria(nombre, descripcion, imagen_url)

    db.session.add(nueva_categoria)
    db.session.commit()
    return categoria_schema.jsonify(nueva_categoria)

@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
    data = request.get_json(force=True)
    actualizar_categoria = Categoria.query.get(id)
    actualizar_categoria.nombre = data['nombre']
    actualizar_categoria.descripcion = data['descripcion']
    actualizar_categoria.imagen_url = data['imagen_url']
    db.session.commit()
    return categoria_schema.jsonify(actualizar_categoria)

@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
    eliminar_categoria = Categoria.query.get(id)
    db.session.delete(eliminar_categoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminar_categoria)

#___Ruta para cargar tarjetas en HTML___
@app.route('/tarjetas', methods=['GET'])
def tarjetas():
    categorias = Categoria.query.all()
    return render_template('tarjetas.html', categorias=categorias)

#___Ruta raíz___
@app.route('/', methods=['GET'])
def root():
    return jsonify({'mensaje': 'Bienvenido'})

#___Ejecutar servidor___
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
