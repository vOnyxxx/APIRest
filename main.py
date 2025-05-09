from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#___Configuracion Server___
usuario_bd ='root'
password_bd = '10503'
servidor_bd = 'localhost'
puerto_bd = '3306'
nombre_bd = 'portal'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"+usuario_bd+":"+password_bd+"@"+servidor_bd+":"+puerto_bd+"/"+nombre_bd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#___Creacion Tablas___
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Categoria(db.Model):
    __tablename__ = "categoria"

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))

    def __init__(self, nombre , descripcion):   
        self.nombre = nombre
        self.descripcion = descripcion

#___Categorias__
#Esquema Tabla Categoria
class CategoriaSchema(ma.SQLAlchemyAutoSchema): 
    class Meta: 
        model = Categoria
        load_instance = True


categoria_schema = CategoriaSchema() 
categorias_schema = CategoriaSchema(many=True)

#GET
@app.route('/categoria', methods = ['GET']) 
def get_categorias():
    all_categorias = Categoria.query.all() 
    result = categorias_schema.dump(all_categorias) 
    return jsonify(result) 
#GET x ID
@app.route('/categoria/<id>', methods = ['GET']) 
def get_categoriaID(id): 
    una_categoria = Categoria.query.get(id) 
    return categoria_schema.jsonify(una_categoria)

#POST
@app.route('/categoria', methods = ['POST']) 
def insert_categoria():
    data = request.get_json(force=True) 
    nombre = data['nombre'] 
    descripcion = data['descripcion'] 

    nueva_categoria = Categoria(nombre, descripcion) 

    db.session.add(nueva_categoria)
    db.session.commit() 
    return categoria_schema.jsonify(nueva_categoria) 

#PUT
@app.route('/categoria/<id>', methods = ['PUT']) 
def update_categoria(id): 
    data = request.get_json(force=True) 
    actualizar_categoria = Categoria.query.get(id) 
    nombre = data['nombre'] 
    descripcion = data['descripcion']

    actualizar_categoria.nombre = nombre 
    actualizar_categoria.descripcion = descripcion 
    db.session.commit() 

    return categoria_schema.jsonify(actualizar_categoria) 

#DELETE
@app.route('/categoria/<id>', methods = ['DELETE']) 
def delete_categoria(id): 
    eliminar_categoria = Categoria.query.get(id) 

    db.session.delete(eliminar_categoria) 
    db.session.commit() 
    return categoria_schema.jsonify(eliminar_categoria) 


#mensaje inicial
@app.route('/', methods = ['GET'])
def root():
    return jsonify({'$mensaje':'Bienvenido'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

