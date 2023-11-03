#Todo lo relacionado a productos de proveedores y revisión de inventario de vendedores.

from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.producto import Prod
from flask_app.models.relacion import Rel
from flask_app.models.vendedor import Ven
from flask_app.models.proveedor import Prov
from flask_app.models.solicitud import Sol
#PARA SUBIR FOTO
from random import sample
from werkzeug.utils import secure_filename 
import os 
from os import remove
from os import path
#TERMINA SUBIR FOTO
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

#PARA ALEATORIO
def stringAleatorio_img():
    #Generando string aleatorio
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio

#Todo lo del proveedor
@app.route('/proveedor/productos/crear')
def start_create():
    return render_template("create_prov.html")

@app.route('/add/producto',methods=['POST'])
def crear_producto():
    if request.method == 'POST':
        if not Prod.validate_prod_add(request.form):
        # redirigimos a la plantilla con el formulario
            return redirect('/proveedor/productos/crear')
    if request.files['new_img_prod']:
        file     = request.files['new_img_prod']
        basepath = "C:\\Users\\ruben\\My_Tools_Management\\flask_app\\" #La ruta donde se encuentra el archivo actual
        filename = secure_filename(file.filename) #Nombre original del archivo
            
        #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
        extension = path.splitext(filename)[1]
        nuevoNombreFile = stringAleatorio_img() + extension
        upload_path = path.join (basepath, 'static/img_prod', nuevoNombreFile) 
        file.save(upload_path)
    else:
        upload_path = ''
    img_prod = 'static/img_prod/'+ nuevoNombreFile
    data = {
        "precio_prod":request.form['new_precio'],
        "nombre_prod": request.form['new_nombre'],
        "descripcion_prod": request.form['new_descripcion'],
        "img_prod": img_prod,
        "proveedor_id": session["user_id"]
    }
    producto_id = Prod.save_prod(data).id
    print("POKEMONS",producto_id)
    data_a = {
        'id_prov': session['user_id']
    }
    for i in Prov.get_vens_by_prov(data_a):
        print(i['id_ven'])
        num = int(i['id_ven'])
        data_b = {
            "producto_id": producto_id,
            "vendedor_id": num
        }
        Rel.save_rel(data_b)
    return redirect('/proveedor/productos')

@app.route('/proveedor/productos/ver/<int:prod_id>')
def start_view(prod_id):
    if 'key_name' in session:
        data_a = {
            'id': prod_id,
        }
        producto = Prod.get_one_prod(data_a)
        print("pikapi",producto)
        return render_template("view_prov.html",prod=producto)
    else:
        return redirect('/')

#PARA EDITAR UN PRODUCTO
@app.route('/proveedor/productos/editar/<int:prod_id>')
def start_edit(prod_id):
    if 'key_name' in session:
        data_a = {
            'id': prod_id,
        }
        producto = Prod.get_one_prod(data_a)
        print("pikapi",producto)
        return render_template("edit_prov.html",prod=producto)
    else:
        return redirect('/')

@app.route('/edit/<int:prod_id>',methods=['POST'])
def editar_producto(prod_id):
    img_prod = ''
    if request.method == 'POST':
        if not Prod.validate_prod_edit(request.form):
        # redirigimos a la plantilla con el formulario
            link = "/proveedor/productos/editar/" + str(prod_id)
            return redirect(link)
    if request.files['edit_img_prod']:
        basepath = "C:\\Users\\ruben\\My_Tools_Management\\flask_app\\" #La ruta donde se encuentra el archivo actual
        data_a = {
            'id': prod_id,
        }
        url_File = path.join (basepath, Prod.get_one_prod(data_a).img_prod)
        if path.exists(url_File):
            remove(url_File)
        #AHORA SE GUARDA LA OTRA IMAGEN
        file     = request.files['edit_img_prod']
        filename = secure_filename(file.filename) #Nombre original del archivo
            
        #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
        extension = path.splitext(filename)[1]
        nuevoNombreFile = stringAleatorio_img() + extension
        upload_path = path.join (basepath, 'static/img_prod', nuevoNombreFile) 
        file.save(upload_path)
        img_prod = 'static/img_prod/'+ nuevoNombreFile
    else:
        basepath = "C:\\Users\\ruben\\My_Tools_Management\\flask_app\\"
        data_a = {
            'id': prod_id,
        }
        img_prod = Prod.get_one_prod(data_a).img_prod
    
    data = {
        "id": prod_id,
        "precio_prod":request.form['edit_precio'],
        "nombre_prod": request.form['edit_nombre'],
        "descripcion_prod": request.form['edit_descripcion'],
        "img_prod": img_prod,
    }
    if request.files['edit_img_prod']:
        Prod.update_prod_x_productos_and_img(data)
    else:
        Prod.update_prod_x_productos(data)
    return redirect('/proveedor/productos')

@app.route('/delete/<int:prod_id>')
def delete(prod_id):
    data = {
        'id': prod_id,
    }
    #Primero eliminamos imagen
    basepath = "C:\\Users\\ruben\\My_Tools_Management\\flask_app\\" #La ruta donde se encuentra el archivo actual
    url_File = path.join (basepath, Prod.get_one_prod(data).img_prod)
    if path.exists(url_File):
        remove(url_File)
    #Ahora se eliminan los datos
    data_b = {
        'producto_id': prod_id,
    }
    data_c = {
        'id_prod_sol': prod_id,
    }
    Sol.destroy_sol_by_prod(data_c)
    Rel.destroy_rels_by_prod(data_b)
    Prod.destroy_prod(data)
    return redirect('/proveedor/productos')

#Todo lo del vendedor