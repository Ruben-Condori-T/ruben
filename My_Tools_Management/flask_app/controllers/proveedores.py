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

def stringAleatorio_cod():
    #Generando string aleatorio
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 8
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio

@app.route('/proveedor')
def proveedor():
    return render_template("proveedor.html")

@app.route('/register/proveedor',methods=['POST'])
def registration_prov():
    if request.method == 'POST':
        if not Prov.validate_prov_reg(request.form):
        # redirigimos a la plantilla con el formulario
            return redirect('/proveedor')
    
    if request.files['perfil_prov']:
        file     = request.files['perfil_prov']
        basepath = "C:\\Users\\ruben\\My_Tools_Management\\flask_app\\" #La ruta donde se encuentra el archivo actual
        filename = secure_filename(file.filename) #Nombre original del archivo
            
        #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
        extension = path.splitext(filename)[1]
        nuevoNombreFile = stringAleatorio_img() + extension
        upload_path = path.join (basepath, 'static/img_prov', nuevoNombreFile) 
        file.save(upload_path)
    else:
        upload_path = ''
    
    pw_hash = bcrypt.generate_password_hash(request.form['password_1a_prov'])
    print(pw_hash)
    img_prov = '../static/img_prov/'+ nuevoNombreFile
    codigo_prov = stringAleatorio_cod()
    data = {
        "first_name_prov":request.form['first_name_prov'],
        "last_name_prov": request.form['last_name_prov'],
        "email_prov": request.form['email_1_prov'],
        "lat_prov": request.form['lat_prov'],
        "lng_prov": request.form['lng_prov'],
        "img_prov": img_prov,
        "password_prov" : pw_hash,
        "codigo_prov" : codigo_prov,
    }
    user_reg = Prov.save_prov(data)
    session["user_id"] = user_reg
    session["key_name"] = "siu"
    return redirect('/proveedor/inicio')

#Validar Login
@app.route('/login/proveedor',methods=['POST'])
def loging_prov():
    if request.method == 'POST':
        if not Prov.getEmail_prov(request.form['email_2_prov']):
            flash("Invalid Email/Password","login_prov")
            return redirect('/proveedor')
        usuario = Prov.getEmail_prov(request.form['email_2_prov'])
        password_prov = request.form['password_2_prov']
        if usuario is None or not bcrypt.check_password_hash(usuario.password_prov, password_prov):
            flash("Invalid Email/Password","login_prov")
            return redirect('/proveedor')
    proveedor = Prov.getEmail_prov(request.form['email_2_prov'])
    session["user_id"] = proveedor.id_prov
    session["key_name"] = "siu"
    return redirect('/proveedor/inicio')

#Dashboard de Proveedor
@app.route('/proveedor/inicio')
def proveedor_inicio():
    data = {
        "id_prov": session["user_id"],
    }
    proveedor=Prov.get_one_prov(data)
    return render_template("dashboard_prov.html",prov=proveedor,all_sols=Prov.get_sols_by_prov(data))

@app.route('/proveedor/productos')
def proveedor_productos():
    data = {
        "id_prov": session["user_id"],
    }
    return render_template("productos_prov.html",all_prods=Prov.get_prods_by_prov(data))

@app.route('/proveedor/inventario')
def proveedor_inventario():
    data = {
        "id_prov": session["user_id"],
    }
    return render_template("inventario_prov.html",all_prods=Prov.get_prods_by_prov(data),all_vens=Prov.get_vens_by_prov(data),i=1)

