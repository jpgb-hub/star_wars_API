import os
from flask import Flask, request, jsonify, abort, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException
from models import db, User, Planet, Character

app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de la base de datos
db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Manejador de errores personalizado
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.ID, 'username': user.username, 'firstname': user.firstname, 'lastname': user.lastname} for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(ID=user_id).first()
    if not user:
        abort(404)
    return jsonify({'id': user.ID, 'username': user.username, 'firstname': user.firstname, 'lastname': user.lastname})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or not data.get('username') or not data.get('password') or not data.get('lastname'):
        abort(400)
    user = User(username=data['username'], password=data['password'], lastname=data['lastname'], firstname=data.get('firstname'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.ID}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.query.filter_by(ID=user_id).first()
    if not user:
        abort(404)
    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        user.password = data['password']
    if 'firstname' in data:
        user.firstname = data['firstname']
    if 'lastname' in data:
        user.lastname = data['lastname']
    db.session.commit()
    return jsonify({'message': 'Usuario actualizado correctamente'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(ID=user_id).first()
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado correctamente'})

# Aquí puedes continuar agregando las rutas para Planetas, Personajes y Favoritos...

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
