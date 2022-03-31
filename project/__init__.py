from distutils.log import Log
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import current_user, login_required, RoleMixin, Security, \
    SQLAlchemyUserDatastore, UserMixin, utils
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib  import sqla

from wtforms.fields import PasswordField

#Creamos una instancia de SQLAlchemy
db=SQLAlchemy()

#Creamos el objeto SQLalchemyUserDataStore
from .models import MateriaPrima, Proveedor, Receta, User, Role, Compra, Venta, Reporte
userDataStore = SQLAlchemyUserDatastore(db,User,Role)

#Método de inicio de la aplicación
def create_app():
    #Creamos una instancia de la clase Flask
    app=Flask(__name__)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    #Generamos la clave aleatoria de sesión Flask para crear una cookie con la inf. de la sesión
    app.config['SECRET_KEY']=os.urandom(24)
    #Definimos la ruta a la BD:
    app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost/ProyectoIntegrador'
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'
    
    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()
        userDataStore.find_or_create_role(name='admin', description='Administrator')
        userDataStore.find_or_create_role(name='empleado', description='Empleado')

    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
        encrypted_password = utils.encrypt_password('password')
        if not userDataStore.get_user('empleado@example.com'):
            userDataStore.create_user(name='empleado',email='empleado@example.com', password=encrypted_password)
        if not userDataStore.get_user('admin@example.com'):
            userDataStore.create_user(name='admin',email='admin@example.com', password=encrypted_password)
        db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
        userDataStore.add_role_to_user('empleado@example.com', 'empleado')
        userDataStore.add_role_to_user('admin@example.com', 'admin')
        db.session.commit()
        
    #Conectando los modelos a flask-security.
    security = Security(app,userDataStore)
    
    #Registremos el blue print para las rutas auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    #Registramos el blue print para las rutas no auth
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    class UserAdmin(sqla.ModelView):

        # Don't display the password on the list of Users
        column_exclude_list = ('password',)

        # Don't include the standard password field when creating or editing a User (but see below)
        form_excluded_columns = ('password',)

        # Automatically display human-readable names for the current and available Roles when creating or editing a User
        column_auto_select_related = True

        # Prevent administration of Users unless the currently logged-in user has the "admin" role
        def is_accessible(self):
            return current_user.has_role('admin')

        # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
        # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
        # we want to use a password field (with the input masked) rather than a regular text field.
        def scaffold_form(self):

            # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
            # password field from this form.
            form_class = super(UserAdmin, self).scaffold_form()

            # Add a password field, naming it "password2" and labeling it "New Password".
            form_class.password2 = PasswordField('New Password')
            return form_class

        # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
        # committed to the database.
        def on_model_change(self, form, model, is_created):

            # If the password field isn't blank...
            if len(model.password2):

                # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
                # the existing password in the database will be retained.
                model.password = utils.encrypt_password(model.password2)
                
    class RoleAdmin(sqla.ModelView):
        # Prevent administration of Roles unless the currently logged-in user has the "admin" role
        def is_accessible(self):
            return current_user.has_role('admin')

    class MateriaPrimaAdmin(sqla.ModelView):
        # Prevent administration of Roles unless the currently logged-in user has the "admin" role
        def is_accessible(self):
            return current_user.has_role('admin')
    
    class RecetaAdmin(sqla.ModelView):
        # Prevent administration of Roles unless the currently logged-in user has the "admin" role
        def is_accessible(self):
            return current_user.has_role('admin')
        
    class ProveedorAdmin(sqla.ModelView):
        # Prevent administration of Roles unless the currently logged-in user has the "admin" role
        def is_accessible(self):
            return current_user.has_role('admin')
    
    class ProveedorAdmin(sqla.ModelView):
        # Prevent administration of Roles unless the currently logged-in user has the "admin" role
        def is_accessible(self):
            return current_user.has_role('admin')
    
    class CompraAdmin(sqla.ModelView):
        # Prevent administration of Roles unless the currently logged-in user has the "admin" role
        def is_accessible(self):
            return current_user.has_role('admin')
    
    class VentaAdmin(sqla.ModelView):
        # Prevent administration of Roles unless the currently logged-in user has the "admin" role
        def is_accessible(self):
            return current_user.has_role('admin')
    
    class ReporteAdmin(sqla.ModelView):
        # Prevent administration of Roles unless the currently logged-in user has the "admin" role
        def is_accessible(self):
            return current_user.has_role('admin')
        
    admin = Admin(app)

    # Add Flask-Admin views for Users and Roles
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(RoleAdmin(Role, db.session))
    admin.add_view(MateriaPrimaAdmin(MateriaPrima, db.session))
    admin.add_view(RecetaAdmin(Receta, db.session))
    admin.add_view(ProveedorAdmin(Proveedor, db.session))
    admin.add_view(CompraAdmin(Compra, db.session))
    admin.add_view(VentaAdmin(Venta, db.session))
    admin.add_view(ReporteAdmin(Reporte, db.session))
    
    return app
    