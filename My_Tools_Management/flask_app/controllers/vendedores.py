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

@app.route('/vendedor')
def vendedor():
    return render_template("vendedor.html")

@app.route('/register/vendedor',methods=['POST'])
def registration_ven():
    if request.method == 'POST':
        if not Ven.validate_ven_reg(request.form):
        # redirigimos a la plantilla con el formulario
            return redirect('/vendedor')
    
    if request.files['perfil_ven']:
        file     = request.files['perfil_ven']
        basepath = "C:\\Users\\ruben\\My_Tools_Management\\flask_app\\" #La ruta donde se encuentra el archivo actual
        filename = secure_filename(file.filename) #Nombre original del archivo
            
        #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
        extension = path.splitext(filename)[1]
        nuevoNombreFile = stringAleatorio_img() + extension
        upload_path = path.join (basepath, 'static/img_ven', nuevoNombreFile) 
        file.save(upload_path)
    else:
        upload_path = ''
    
    pw_hash = bcrypt.generate_password_hash(request.form['password_1a_ven'])
    print(pw_hash)
    img_ven = path.join('../static/img_ven/', nuevoNombreFile)

    #Buscar proveedor por código
    proveedor_id=Prov.get_by_codigo(request.form['codigo_prov']).id_prov

    data = {
        "first_name_ven":request.form['first_name_ven'],
        "last_name_ven": request.form['last_name_ven'],
        "email_ven": request.form['email_1_ven'],
        "proveedor_id": proveedor_id,
        "lat_ven": request.form['lat_ven'],
        "lng_ven": request.form['lng_ven'],
        "img_ven": img_ven,
        "password_ven" : pw_hash
    }
    user_reg = Ven.save_ven(data)
    session["user_id"] = user_reg
    session["key_name"] = "siu"
    data_a = {
        'id_prov': proveedor_id
    }
    for i in Prov.get_prods_by_prov(data_a):
        num = i["id"]
        data_b = {
            "producto_id": num,
            "vendedor_id": session["user_id"]
        }
        Rel.save_rel(data_b)
    return redirect('/vendedor/inicio')


#Validar Login
@app.route('/login/vendedor',methods=['POST'])
def loging_ven():
    if request.method == 'POST':
        if not Ven.getEmail_ven(request.form['email_2_ven']):
            flash("Invalid Email/Password","login_ven")
            return redirect('/vendedor')
        usuario = Ven.getEmail_ven(request.form['email_2_ven'])
        password_ven = request.form['password_2_ven']
        if usuario is None or not bcrypt.check_password_hash(usuario.password_ven, password_ven):
            flash("Invalid Email/Password","login_ven")
            return redirect('/vendedor')
    vendedor = Ven.getEmail_ven(request.form['email_2_ven'])
    session["user_id"] = vendedor.id_ven
    session["key_name"] = "siu"
    data = {
        'id_ven': session["user_id"]
    }
    solicitudes = Ven.get_sols_by_ven(data)
    for solicitud in solicitudes:
        if solicitud['tiempo_sol'] == 1:
            data_a = {
                'id_sol': solicitud['id_sol']
            }
            Sol.destroy_one_sol(data_a)
    return redirect('/vendedor/inicio')

#Dashboard de Proveedor
@app.route('/vendedor/inicio')
def vendedor_inicio():
    data = {
        "id_ven": session["user_id"],
    }
    vendedor=Ven.get_one_ven(data)
    data_b = {
        "id_prov": Ven.get_one_ven(data).proveedor_id
    }
    proveedor=Prov.get_one_prov(data_b)
    productos=Prov.get_prods_by_prov(data_b)
    return render_template("dashboard_ven.html",ven=vendedor, prov=proveedor,all_prods=productos, all_sols=Ven.get_sols_by_ven(data) )