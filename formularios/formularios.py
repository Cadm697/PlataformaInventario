from flask_wtf import FlaskForm
import flask_wtf
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.widgets.core import SubmitInput

class Usuario(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired("Debe ingresar el nombre")])
    apellido = StringField("Apellido", validators=[DataRequired("Debe ingresar el apellido")])
    cedula = StringField("cedula", validators=[DataRequired("Debe ingresar la cedula")])
    celular = StringField("Celular")
    id_cat = SelectField("Categoria")
    contraseña = PasswordField("Contraseña", validators=[DataRequired("Debe ingresar una contraseña")])
    guardar = SubmitField("Guardar")
    
class Proveedor(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired("Debe ingresar el nombre")])
    nit = StringField("NIT", validators=[DataRequired("Debe ingresar el NIT")])
    telefono = StringField("telefono", validators=[DataRequired("Debe ingresar el numero de telefono")])
    correo = StringField("Correo electronico")
    guardar = SubmitField("Guardar")

class Producto(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired("Debe ingresar el nombre")])
    descripcion = StringField("Descripcion")
    cantidad_minima = StringField("Cantidad minima", validators=[DataRequired("Debe ingresar la cantidad minima")])
    cantidad_bodega = StringField("Cantidad bodega", validators=[DataRequired("Debe ingresar la cantidad bodega")])
    id_proveedor = SelectField("Id Proveedor")
    guardar = SubmitField("Guardar")
    
class Login(FlaskForm):
    cedula = StringField("Cedula", validators=[DataRequired("Debe ingresar una cedula")])
    contraseña = PasswordField("Contraseña", validators=[DataRequired("Debe ingresar una contraseña")])
    iniciar = SubmitField("Iniciar sesión")