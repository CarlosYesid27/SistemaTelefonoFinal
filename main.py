from flask import Flask, flash, render_template,request,redirect,Response,session, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import sqlite3
from functools import wraps
from datetime import datetime
import os
from flask import send_from_directory



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
CARPETA = os.path.join('static', 'uploads')
app.config['CARPETA'] = CARPETA
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(80), nullable = False)


mysql = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'telefonofinal'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))  # <-- Cambia aquí
        else:
            error = 'Usuario o contraseña incorrectos'
    return render_template('modulos/telefonos/login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            error = 'El usuario ya existe'
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('modulos/telefonos/register.html', error=error)

@app.route('/telefonos')
@login_required
def index_telefonos():
    sql = "SELECT * FROM telefonos;"
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql)
    telefonos = cursor.fetchall()
    conexion.commit()
    return render_template('modulos/telefonos/index.html', telefonos = telefonos)


@app.route('/registrar')
def create():
    return render_template('modulos/telefonos/create.html')


@app.route('/telefonos/create')
def create2():
    return render_template('modulos/telefonos/create.html')


@app.route('/registrar/guardar', methods = ['POST'])
def guardar():
    marca = request.form['marca']
    modelo = request.form['modelo']
    num_sim = request.form['numero sim']
    imei = request.form['imei']
    fecha = request.form['fecha de registro']
    foto = request.files['foto']
    if marca == '' or modelo == '' or num_sim == '' or imei == '' or fecha == '' or foto.filename == '':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('create'))
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    nuevoNombreFoto = ""
    if foto.filename != '':
        nuevoNombreFoto = tiempo + foto.filename
        foto.save(os.path.join(app.config['CARPETA'], nuevoNombreFoto))

    sql = "INSERT INTO telefonos(marca, modelo, numero_sim, imei,fecha_registro, foto) VALUES(%s, %s, %s, %s, %s, %s)"
    datos = (marca, modelo, num_sim, imei, fecha, nuevoNombreFoto)
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/telefonos')

@app.route('/telefonos/edit/<int:id>')
def telefonos_editar(id):
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM telefonos WHERE id=%s", (id,))
    telefonos = cursor.fetchone()
    conexion.commit()
    return render_template('modulos/telefonos/edit.html', telefonos = telefonos)

@app.route('/telefonos/edit/actualizar', methods = ['POST'])
def telefonos_actualizar():
    id = request.form['txtid']
    marca = request.form['marca']
    modelo = request.form['modelo']
    num_sim = request.form['numero sim']
    imei = request.form['imei']
    fecha = request.form['fecha de registro']
    foto = request.files['foto']

    sql = "UPDATE telefonos SET marca=%s, modelo=%s, numero_sim=%s, imei=%s, fecha_registro=%s WHERE id=%s"
    datos = (marca, modelo, num_sim, imei, fecha, id)
    conexion = mysql.connection
    cursor = conexion.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    if foto and foto.filename != '':
        nuevoNombreFoto = tiempo + foto.filename
        foto.save(os.path.join(app.config['CARPETA'], nuevoNombreFoto))

        cursor.execute("SELECT foto FROM telefonos WHERE id=%s", (id,))
        fila = cursor.fetchone()
        if fila and fila['foto']:
            try:
                os.remove(os.path.join(app.config['CARPETA'], fila['foto']))
            except Exception:
                pass
        cursor.execute("UPDATE telefonos SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))
        conexion.commit()

    cursor.execute(sql, datos)
    conexion.commit()
    return redirect('/telefonos')

@app.route('/telefonos/borrar/<int:id>')
def telefonos_borrar(id):
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("SELECT foto FROM telefonos WHERE id=%s", (id,))
    fila = cursor.fetchone()
    if fila and fila['foto']:
        try:
            os.remove(os.path.join(app.config['CARPETA'], fila['foto']))
        except Exception:
            pass
    cursor.execute("DELETE FROM telefonos WHERE id=%s", (id,))
    conexion.commit()
    return redirect('/telefonos')


@app.route('/dashboard')
@login_required
def dashboard():
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("SELECT marca, COUNT(*) as cantidad FROM telefonos GROUP BY marca;")
    resultados = cursor.fetchall()
    labels = [row['marca'] for row in resultados]
    data = [row['cantidad'] for row in resultados]
    total_telefonos = sum(data)

    # Total usuarios
    total_usuarios = User.query.count()
    # Último teléfono
    cursor.execute("SELECT * FROM telefonos ORDER BY id DESC LIMIT 1;")
    ultimo_telefono = cursor.fetchone()
    # Último usuario
    ultimo_usuario = User.query.order_by(User.id.desc()).first()

    # Teléfonos por mes (para la gráfica de barras)
    cursor.execute("""
        SELECT DATE_FORMAT(fecha_registro, '%m-%Y') as mes, COUNT(*) as cantidad
        FROM telefonos
        GROUP BY mes
        ORDER BY STR_TO_DATE(mes, '%m-%Y')
    """)
    resultados_mes = cursor.fetchall()
    meses = [row['mes'] for row in resultados_mes]
    telefonos_por_mes = [row['cantidad'] for row in resultados_mes]

    return render_template(
        'dashboard.html',
        labels=labels,
        data=data,
        total_telefonos=total_telefonos,
        total_usuarios=total_usuarios,
        ultimo_telefono=ultimo_telefono,
        ultimo_usuario=ultimo_usuario,
        meses=meses,
        telefonos_por_mes=telefonos_por_mes
    )


if __name__ == '__main__':
    app.secret_key = "carlos_at"
    app.run(debug=True)
