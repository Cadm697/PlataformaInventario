from flask import Flask, render_template, flash, session, request
import sqlite3
import os
import hashlib
from flask.helpers import flash
from werkzeug.utils import redirect, escape

from wtforms.compat import with_metaclass

from formularios.formularios import Usuario, Proveedor, Producto, Login

app=Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def home():
    frm = Login()
    if frm.validate_on_submit():
        cedula = escape(frm.cedula.data)
        contraseña = escape(frm.contraseña.data)
        #ciframos la contraseña para compararla
        enc = hashlib.sha256(contraseña.encode())
        pass_enc = enc.hexdigest()
        with sqlite3.connect("inventario.db") as con:
        #Convierte la respuesta de la consulta en un diccionario
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT categoria FROM usuario WHERE cedula = ? AND contraseña = ?", [cedula, pass_enc])
            if cursor.fetchall:
                row = cursor.fetchall()
                session["categoria"] = row[0]["categoria"]
                #boton = True;
                #return render_template("base.html", boton = boton)
                return redirect("/productos")
            else:
                flash("cedula/contraseña errados")
                return render_template("login.html", frm = frm)
    return render_template("login.html", frm = frm)

@app.route("/usuarios/registrar", methods=["GET", "POST"]) 
def registrarUsuario():
    if session["categoria"] == "Administrador" or session["categoria"] == "Superdministrador":
        frm = Usuario()
        if frm.validate_on_submit():
            nombre = frm.nombre.data
            apellido = frm.apellido.data
            cedula = frm.cedula.data
            celular = frm.celular.data
            categoria = frm.categoria.data
            contraseña = frm.contraseña.data
            enc = hashlib.sha256(contraseña.encode())
            pass_enc = enc.hexdigest()
            with sqlite3.connect("inventario.db") as con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO usuario (nombre, apellido, cedula, celular, categoria, contraseña) VALUES (?,?,?,?,?,?)",
                            [nombre, apellido, cedula, celular, categoria, pass_enc])
                con.commit()
                flash("Usuario Guardado con exito")
                return redirect("/usuarios")
        else:
            return render_template("registro.html", frm = frm)
    else:
        flash("No tienes acceso para crear usuarios")
        return redirect("/productos")
    
@app.route("/usuarios", methods=["GET"])
def listarUsuarios():
    if session["categoria"] == "Administrador" or session["categoria"] == "Superdministrador":
        with sqlite3.connect("inventario.db") as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT codigo, nombre, apellido, cedula, celular, categoria FROM usuario")
            rows = cursor.fetchall()
            return render_template("usuarios.html", rows = rows)
    else:
        flash("No tienes acceso la lista de usuarios")
        return redirect("/productos")

@app.route("/usuarios/eliminar/<int:codigo>", methods=["GET"])
def eliminarUsuario(codigo):
    if session["categoria"] == "Administrador" or session["categoria"] == "Superdministrador":
        with sqlite3.connect("inventario.db") as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM usuario WHERE codigo = ?", [codigo])
            con.commit()
            flash("El Usuario se ha eliminado")
        return redirect("/usuarios")
    else:
        flash("No tienes acceso para eliminar usuarios")
        return redirect("/productos")

@app.route("/usuarios/editar/<int:codigo>", methods=["GET","POST"])
def editarUsuario(codigo):
    if session["categoria"] == "Administrador" or session["categoria"] == "Superdministrador":
        frm = Usuario()
        if frm.validate_on_submit():
            nombre = frm.nombre.data
            apellido = frm.apellido.data
            cedula = frm.cedula.data
            celular = frm.celular.data
            categoria = frm.categoria.data
            contraseña = frm.contraseña.data
            enc = hashlib.sha256(contraseña.encode())
            pass_enc = enc.hexdigest()
            with sqlite3.connect("inventario.db") as con:
                cursor = con.cursor()
                cursor.execute("UPDATE usuario SET nombre=?, apellido=?, cedula=?, celular=?, categoria=?, contraseña=? WHERE codigo=?",
                            [nombre, apellido, cedula, celular, categoria, pass_enc, codigo])
                con.commit()
                flash("Usuario Guardado con exito")
                return redirect("/usuarios")
        else:
            with sqlite3.connect("inventario.db") as con:
                #Convierte la respuesta de la consulta en un diccionario
                con.row_factory = sqlite3.Row
                cursor = con.cursor()
                cursor.execute("SELECT * FROM usuario WHERE codigo = ?", [codigo])
                row = cursor.fetchone()
                frm.nombre.data = row["nombre"]
                frm.apellido.data = row["apellido"]
                frm.cedula.data = row["cedula"]
                frm.celular.data = row["celular"]
                frm.categoria.data = row["categoria"]
                frm.contraseña.data = row["contraseña"]
            return render_template("registro.html", frm = frm)
    else:
        flash("No tienes acceso para editar usuarios")
        return redirect("/productos")

@app.route("/proveedores/registrar", methods=["GET", "POST"]) 
def registrarProveedor():
    frm = Proveedor()
    if frm.validate_on_submit():
        nombre = frm.nombre.data
        nit = frm.nit.data
        telefono = frm.telefono.data
        correo = frm.correo.data
        with sqlite3.connect("inventario.db") as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO proveedor (nombre, nit, telefono, correo) VALUES (?,?,?,?)", [nombre, nit, telefono, correo])
            con.commit()
            flash("Proveedor guardado con exito")
            return redirect("/proveedores")
    else:
        return render_template("regProveedor.html", frm = frm)

@app.route("/proveedores", methods=["GET"])
def listarProveedores():
    with sqlite3.connect("inventario.db") as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM proveedor")
        rows = cursor.fetchall()
        return render_template("proveedores.html", rows = rows)

@app.route("/proveedores/eliminar/<int:id>", methods=["GET"])
def eliminarProveedor(id):
        with sqlite3.connect("inventario.db") as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM proveedor WHERE id = ?", [id])
            con.commit()
            flash("El proveedor se ha eliminado")
        return redirect("/proveedores")

@app.route("/proveedores/editar/<int:id>", methods=["GET","POST"])
def editarProveedor(id):
    frm = Proveedor()
    if frm.validate_on_submit():
        nombre = frm.nombre.data
        nit = frm.nit.data
        telefono = frm.telefono.data
        correo = frm.correo.data
        with sqlite3.connect("inventario.db") as con:
            cursor = con.cursor()
            cursor.execute("UPDATE proveedor SET nombre=?, nit=?, telefono=?, correo=? WHERE id=?",
                           [nombre, nit, telefono, correo, id])
            con.commit()
            flash("Proveedor Actualizado con exito")
            return redirect("/proveedores")
    else:
        with sqlite3.connect("inventario.db") as con:
            #Convierte la respuesta de la consulta en un diccionario
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT * FROM proveedor WHERE id = ?", [id])
            row = cursor.fetchone()
            frm.nombre.data = row["nombre"]
            frm.nit.data = row["nit"]
            frm.telefono.data = row["telefono"]
            frm.correo.data = row["correo"]
        return render_template("regProveedor.html", frm = frm)

@app.route("/productos/registrar", methods=["GET", "POST"]) 
def registrarProducto():
    frm = Producto()
    if frm.validate_on_submit():
        nombre = frm.nombre.data
        descripcion = frm.descripcion.data
        cantidad_minima = frm.cantidad_minima.data
        cantidad_bodega = frm.cantidad_bodega.data
        id_proveedor = frm.id_proveedor.data
        
        if cantidad_minima.isnumeric() != True:
            flash("La cantidad minima debe ser un numero")
            return render_template("regProducto.html", frm = frm)
        elif cantidad_bodega.isnumeric() != True:
            flash("La cantidad en bodega debe ser un numero")
            return render_template("regProducto.html", frm = frm)
        else:
            with sqlite3.connect("inventario.db") as con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO producto (nombre, descripcion, cantidad_minima, cantidad_bodega, id_proveedor) VALUES (?,?,?,?,?)",
                            [nombre, descripcion, cantidad_minima, cantidad_bodega, id_proveedor])
                con.commit()
                flash("Producto guardado con exito")
                return redirect("/productos")
    else:
        return render_template("regProducto.html", frm = frm)

@app.route("/productos", methods=["GET"])
def listarProductos():
    with sqlite3.connect("inventario.db") as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM producto")
        rows = cursor.fetchall()
        return render_template("productos.html", rows = rows)

@app.route("/productos/eliminar/<int:id>", methods=["GET"])
def eliminarProducto(id):
        with sqlite3.connect("inventario.db") as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM producto WHERE id = ?", [id])
            con.commit()
            flash("El producto se ha eliminado")
        return redirect("/productos")

@app.route("/productos/editar/<int:id>", methods=["GET","POST"])
def editarProducto(id):
    frm = Producto()
    if frm.validate_on_submit():
        nombre = frm.nombre.data
        descripcion = frm.descripcion.data
        cantidad_minima = frm.cantidad_minima.data
        cantidad_bodega = frm.cantidad_bodega.data
        id_proveedor = frm.id_proveedor.data
        with sqlite3.connect("inventario.db") as con:
            cursor = con.cursor()
            cursor.execute("UPDATE producto SET nombre=?, descripcion=?, cantidad_minima=?, cantidad_bodega=?, id_proveedor=? WHERE id=?",
                           [nombre, descripcion, cantidad_minima, cantidad_bodega, id_proveedor, id])
            con.commit()
            flash("Producto Actualizado con exito")
            return redirect("/productos")
    else:
        with sqlite3.connect("inventario.db") as con:
            #Convierte la respuesta de la consulta en un diccionario
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT * FROM producto WHERE id = ?", [id])
            row = cursor.fetchone()
            frm.nombre.data = row["nombre"]
            frm.descripcion.data = row["descripcion"]
            frm.cantidad_minima.data = row["cantidad_minima"]
            frm.cantidad_bodega.data = row["cantidad_bodega"]
            frm.id_proveedor.data = row["id_proveedor"]
        return render_template("regProducto.html", frm = frm)

@app.route("/productos/porpedir", methods=["GET"])
def listarPorPedirProductos():
    with sqlite3.connect("inventario.db") as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM producto WHERE cantidad_minima >= cantidad_bodega")
        pedir = cursor.fetchall()
        return render_template("productos.html", pedir = pedir)

@app.route("/logout")
def logoute():
    session.clear()
    return redirect("/")

app.run(debug=True)