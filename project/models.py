from sqlalchemy import Column, ForeignKey
from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

#Definiendo la tabla relacional
users_roles=db.Table('users_roles',
                     db.Column('userId', db.Integer, db.ForeignKey('user.id')),
                     db.Column('roleId', db.Integer, db.ForeignKey('role.id')))

#Definimos la clase del usuario
class User(UserMixin, db.Model):
    """"User account model"""
    
    _tablename_='user'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100), unique=True)
    password=db.Column(db.String(255), nullable=False)
    active=db.Column(db.Boolean)
    confirmed_at=db.Column(db.DateTime)
    roles=db.relationship('Role', 
                           secondary=users_roles,
                           backref=db.backref('users', lazy='dynamic'))
    
class Role(RoleMixin, db.Model):
    """Role model"""
        
    __tablename__='role'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    
materia_recetas=db.Table('materiaPrima_recetas',
                     db.Column('materiaPrimaId', db.Integer, db.ForeignKey('materiaPrima.id')),
                     db.Column('recetaId', db.Integer, db.ForeignKey('receta.id')))    
    
class MateriaPrima(db.Model):
    """Materia Prima model"""
    
    __tablename__ = 'materiaPrima'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    gramaje= db.Column(db.Float, nullable=False)
    pieza= db.Column(db.Integer, nullable=False)
    estatus=db.Column(db.Boolean)
    
class Receta(db.Model):
    """Receta model"""
    
    __tablename__='receta'
    id = db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50), nullable=False)
    precio=db.Column(db.Float, nullable=False)
    imagen=db.Column(db.String(500), nullable=False)
    estatus=db.Column(db.Boolean)
    materia=db.relationship('MateriaPrima', 
                           secondary=materia_recetas,
                           backref=db.backref('recetas', lazy='dynamic'))
    
proveedores_compras=db.Table('proveedores_compras',
                     db.Column('proveedorId', db.Integer, db.ForeignKey('proveedor.id')),
                     db.Column('compraId', db.Integer, db.ForeignKey('compra.id')))  
    
class Proveedor(db.Model):
    """Proveedor model"""
    
    __tablename__='proveedor'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50), nullable=False)
    dirección=db.Column(db.String(50), nullable=False)
    codigoPostal=db.Column(db.Integer, nullable=False)
    ciudad=db.Column(db.String(50), nullable=False)
    rfc=db.Column(db.String(13), nullable=False)
    telefono=db.Column(db.Integer, nullable=False)
    
class Compra(db.Model):
   """Compra model""" 
   __tablename__='compra'
   id=db.Column(db.Integer, primary_key=True)
   nombre=db.Column(db.String(50), nullable=False)
   cantidad=db.Column(db.Float, nullable=False)
   costo=db.Column(db.Float, nullable=False)
   fecha=db.Column(db.Date, nullable=False)
   estatus=db.Column(db.Boolean)
   proveedor=db.relationship('Proveedor', 
                           secondary=proveedores_compras,
                           backref=db.backref('compras', lazy='dynamic'))

recetas_ventas=db.Table('recetas_ventas',
                     db.Column('recetaId', db.Integer, db.ForeignKey('receta.id')),
                     db.Column('ventaId', db.Integer, db.ForeignKey('venta.id')))  

class Venta(db.Model):
    """Venta model"""
    
    __tablename__='venta'
    id=db.Column(db.Integer, primary_key=True)
    nombreProducto=db.relationship('Receta', 
                          secondary=recetas_ventas,
                          backref=db.backref('ventas', lazy='dynamic'))
    cantidad=db.Column(db.Integer, nullable=False)
    fecha=db.Column(db.Date,nullable=False)
    total=db.Column(db.Float,nullable=False)
    estatus=db.Column(db.Boolean)
    
compras_reportes=db.Table('compras_reportes',
                     db.Column('compraId', db.Integer, db.ForeignKey('compra.id')),
                     db.Column('reporteId', db.Integer, db.ForeignKey('reporte.id'))) 

ventas_reportes=db.Table('ventas_reportes',
                     db.Column('ventaId', db.Integer, db.ForeignKey('venta.id')),
                     db.Column('reporteId', db.Integer, db.ForeignKey('reporte.id')))  
    
class Reporte(db.Model):
    """Reporte model"""
    
    __tablename__='reporte'
    id=db.Column(db.Integer, primary_key=True)
    compra=db.relationship('Compra', 
                           secondary=compras_reportes,
                           backref=db.backref('reportes', lazy='dynamic'))
    venta=db.relationship('Venta', 
                           secondary=ventas_reportes,
                           backref=db.backref('reportes', lazy='dynamic'))