from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "secret_key"  # Clave para manejar sesiones

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gymapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos de base de datos
class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    ejercicio = db.Column(db.String(80), nullable=False)
    peso_kg = db.Column(db.Float, nullable=False)
    repeticiones = db.Column(db.Integer, nullable=False)
    series = db.Column(db.Integer, nullable=False)

# Crear tablas y usuario de prueba
with app.app_context():
    db.create_all()
    if not UserAccount.query.filter_by(username="testuser").first():
        user = UserAccount(username="testuser", password="password123")
        db.session.add(user)
        db.session.commit()

# Landpage
@app.route('/')
def index():
    return redirect(url_for('login'))  # Redirige a la página de login

# Registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            if UserAccount.query.filter_by(username=username).first():
                return "El usuario ya existe"
            user = UserAccount(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

# Inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserAccount.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return "Credenciales incorrectas"
    return render_template('login.html')

# Tablero principal
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    exercises = Exercise.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', exercises=exercises)

# Agregar un ejercicio
@app.route('/add-exercise', methods=['GET', 'POST'])
def add_exercise():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        ejercicio = request.form['ejercicio']
        fecha = datetime.strptime(request.form['fecha'], '%d/%m/%Y')
        peso_kg = float(request.form['peso_kg'])
        repeticiones = int(request.form['repeticiones'])
        series = int(request.form['series'])
        if all([ejercicio, fecha, peso_kg, repeticiones, series]):
            exercise = Exercise(
                user_id=session['user_id'],
                fecha=fecha,
                ejercicio=ejercicio,
                peso_kg=peso_kg,
                repeticiones=repeticiones,
                series=series
            )
            db.session.add(exercise)
            db.session.commit()
            return redirect(url_for('dashboard'))
    return render_template('add_exercise.html')

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)