from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os




app = Flask(__name__)

# Configuración de la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Por defecto, el usuario es root
app.config['MYSQL_PASSWORD'] = ''  # Por defecto, no hay contraseña
app.config['MYSQL_DB'] = 'uw'

# Clave secreta para la sesión
app.config['SECRET_KEY'] = 'your_secret_key'

# Inicializar MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO usuariocontra (username, password) VALUES (%s, %s)', (username, password))
        mysql.connection.commit()
        cursor.close()
        flash('Registro exitoso')
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuariocontra WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            flash('inicio de sesion correcto')
        else:
            flash('Usuario o contraseña incorrecta')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
