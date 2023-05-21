"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/todos", methods=['GET', 'POST'])  # Aquí especificamos que estos endpoints aceptan solicitudes POST y GET.
def get_todos():
    response_body = [
                        {
                            "done": "true",
                            "label": "Sample Todo 1"
                        },
                        {
                            "done": "true",
                            "label": "Sample Todo 2"
                        }
                    ]
    if request.method == 'GET':  # Podemos entender qué tipo de request estamos manejando usando un condicional

        return jsonify(response_body), 200
    
    body = request.get_json()  # Obtener el request body de la solicitud
    response_body.append(body)
    return jsonify(response_body), 200

@app.route('/todos/<int:todo_index>', methods=['DELETE'])
def delete_todo(todo_index):
    todo_index = int(todo_index)
    if (todo_index < 0 or todo_index > 2) : return 'Introduzca numeros naturales'
    data = [
                {
                    "done": "true",
                    "label": "Sample Todo 1"
                },
                {
                    "done": "true",
                    "label": "Sample Todo 2"
                },
                {
                    "done": "true",
                    "label": "Sample Todo 3"
                }
            ]
    # response = list(filter(lambda val: todo_index == val['label'], data))
    if todo_index < len(data):
        del data[todo_index]

    return data, 200

    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
