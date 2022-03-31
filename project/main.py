from flask import Blueprint,Flask, render_template
from flask_security import login_required, current_user, utils
from flask_security.decorators import roles_required
import logging
from datetime import datetime
from . import db
from flask_admin import Admin
from flask_admin.contrib  import sqla
from wtforms import PasswordField

main = Blueprint('main', __name__)

#Definimos la ruta principal
@main.route('/')
@login_required
def index():
    app = Flask(__name__)
    #Registrar Log para el inicio de la aplicacion
    fechaActual=datetime.now()
    fecha="{}:{}:{}".format(fechaActual.day, fechaActual.month, fechaActual.year)
    hora="{}:{}".format(fechaActual.hour, fechaActual.minute)
    app.logger.debug('Fecha: {} Hora: {} Inicio de la aplicacion'.format(fecha,hora))
    log=str(app.logger.debug('Fecha: {} Hora: {} Inicio de la aplicacion'.format(fecha,hora)))
    LOG_FILENAME = 'registro.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG),log
    return render_template('index.html')

#Definimos la ruta a la página de perfil
@main.route('/profile')
@login_required
#@roles_required('admin')#Autorización para el rol admin
def profile():
    return render_template('profile.html', name=current_user.name)
