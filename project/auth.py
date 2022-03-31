from flask import Blueprint, Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user
from .models import User
from . import db, userDataStore
import logging
from datetime import datetime

auth = Blueprint('auth', __name__, url_prefix='/security')

#GET
@auth.route('/login')
def login():
    return render_template('/security/login.html')

#POST
@auth.route('/login',methods=['POST'])
def login_post():
    app=Flask(__name__)
    email=request.form.get('email')
    password=request.form.get('password')
    remember= True if request.form.get('remember') else False
    
    #Consultamos si existe un usuario ya registrado
    user=User.query.filter_by(email=email).first()
    
    #Verificamos si el usuario existe.
    #Tomamos el password proporcionado por el usuario
    if not user or not check_password_hash(user.password, password):
        flash('El usuario y/o la password son incorrectos')       
        fechaActual=datetime.now()
        fecha="{}:{}:{}".format(fechaActual.day, fechaActual.month, fechaActual.year)
        hora="{}:{}".format(fechaActual.hour, fechaActual.minute)
        app.logger.error('Fecha: {} Hora: {} El usuario y/o la contraseña son incorrectos'.format(fecha,hora))
        log=str(app.logger.error('Fecha: {} Hora: {} El usuario y/o la contraseña son incorrectos'.format(fecha,hora)))
        LOG_FILENAME = 'registro.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG),log
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    fechaActual=datetime.now()
    fecha="{}:{}:{}".format(fechaActual.day, fechaActual.month, fechaActual.year)
    hora="{}:{}".format(fechaActual.hour, fechaActual.minute)
    app.logger.debug('Fecha: {} Hora: {} Acceso de: {}'.format(fecha,hora,email))
    log=str(app.logger.debug('Fecha: {} Hora: {} Acceso de: {}'.format(fecha,hora,email)))
    LOG_FILENAME = 'registro.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG),log
    return redirect(url_for('main.profile'))

@auth.route('/register')
def register():
    return render_template('/security/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    app = Flask(__name__)
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    #Consultamos si existe un usuario ya registrado
    user = User.query.filter_by(email=email).first()
    
    if user: #Si se encontró un usuario ya registrado
        fechaActual=datetime.now()
        fecha="{}:{}:{}".format(fechaActual.day, fechaActual.month, fechaActual.year)
        hora="{}:{}".format(fechaActual.hour, fechaActual.minute)
        app.logger.error('Fecha: {} Hora: {} Se quizo hacer un registro con un correo existente'.format(fecha,hora))
        log=str(app.logger.error('Fecha: {} Hora: {}  Se quizo hacer un registro con un correo existente'.format(fecha,hora)))
        LOG_FILENAME = 'registro.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG),log
        return redirect(url_for('auth.register'))
    
    #Si no existe, creamos un nuevo usuario con sus datos
    #Hacemos un hash a la contraseña para protegerla.
    #new_user= User(email=email, name=name, 
    #password=generate_password_hash(password, method='sha256'))
    userDataStore.create_user(
        name=name, email=email, password=generate_password_hash(password,method='sha256')
    )
    
    #Añadimos el nuevo usuario a la base de datos
    #db.session.add(new_user)
    db.session.commit()
    
    #Redireccionamos a la vista de login
    return redirect(url_for('auth.login'))        

@auth.route('/logout')
@login_required
def logout():
    #Cerramos la sesión
    logout_user()
    return redirect(url_for('main.index'))