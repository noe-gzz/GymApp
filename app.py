from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la base de datos remota en Railway.app (asegúrate de actualizar la URL de la base de datos)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:lDZoCulwdCFVFykQGsNliXsBSsImCfNb@postgres.railway.internal:5432/railway') # Usa SQLite como respaldo local
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de SQLAlchemy
db = SQLAlchemy(app)

# Definición del modelo de la tabla Ejercicios
class Ejercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ejercicio = db.Column(db.String(100), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    repeticion = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.String(50), nullable=False)

# Ruta principal (bienvenida)
@app.route('/')
def index():
    return jsonify({"mensaje": "Bienvenido a la API del GymApp"})

# Endpoint para agregar un ejercicio
@app.route('/ejercicios', methods=['POST'])
def agregar_ejercicio():
    datos = request.json
    nuevo_ejercicio = Ejercicio(
        ejercicio=datos['ejercicio'],
        peso=datos['peso'],
        repeticion=datos['repeticion'],
        fecha=datos['fecha']
    )
    db.session.add(nuevo_ejercicio)
    db.session.commit()
    return jsonify({"mensaje": "Ejercicio agregado con éxito"})

# Endpoint para obtener todos los ejercicios
@app.route('/ejercicios', methods=['GET'])
def obtener_ejercicios():
    ejercicios = Ejercicio.query.all()
    resultado = [
        {"id": e.id, "ejercicio": e.ejercicio, "peso": e.peso, "repeticion": e.repeticion, "fecha": e.fecha}
        for e in ejercicios
    ]
    return jsonify(resultado)

# Endpoint para actualizar un ejercicio
@app.route('/ejercicios/<int:id>', methods=['PUT'])
def actualizar_ejercicio(id):
    datos = request.json
    ejercicio = Ejercicio.query.get_or_404(id)
    ejercicio.ejercicio = datos['ejercicio']
    ejercicio.peso = datos['peso']
    ejercicio.repeticion = datos['repeticion']
    ejercicio.fecha = datos['fecha']
    db.session.commit()
    return jsonify({"mensaje": "Ejercicio actualizado con éxito"})

# Endpoint para eliminar un ejercicio
@app.route('/ejercicios/<int:id>', methods=['DELETE'])
def eliminar_ejercicio(id):
    ejercicio = Ejercicio.query.get_or_404(id)
    db.session.delete(ejercicio)
    db.session.commit()
    return jsonify({"mensaje": "Ejercicio eliminado con éxito"})

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)