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

@app.route('/solicitar/producto/<int:id_ven>',methods=['POST'])
def solicitar_producto(id_ven):
    if request.method == 'POST':
        is_valid=True
        cantidad_sol = int(request.form['cantidad_sol'])
        data_x = {
            'id': int(request.form['id_prod_sol'])
        }
        cantidad_x_prov = int(Prod.get_one_prod(data_x).cantidad_x_prov)
        cantidad_en_ven = int(Prod.get_one_prod(data_x).cantidad_en_ven)
        cantidad_en_stock = cantidad_x_prov - cantidad_en_ven
        factor = cantidad_en_stock - cantidad_sol
        if len(request.form['razon_sol']) < 8:
            flash("La contraseña debe contar con al menos 8 caracteres","soliciting")
            is_valid=False
        if factor<0:
            flash("Usted no puede exigir dicha cantidad de productos, intente con una menor cantidad","soliciting")
            is_valid=False
        if is_valid:
            data_y = {
                'id_ven': session["user_id"]
            }
            vendedor = Ven.get_one_ven(data_y)
            data = {
                "cantidad_sol":request.form['cantidad_sol'],
                "razon_sol": request.form['razon_sol'],
                "id_prod_sol": request.form['id_prod_sol'],
                "vendedor_id": session["user_id"],
                "proveedor_id": vendedor.proveedor_id
            }
            Sol.save_sol(data)
        return redirect("/vendedor/inicio")

@app.route('/aceptar/solicitud/<int:id_sol>')
def aceptar_solicitud(id_sol):
    data_a = {
        'id_sol': id_sol
    }
    solicitud = Sol.get_one_sol(data_a)
    data_prod = {
        'id': solicitud.id_prod_sol
    }
    data_rel = {
        'vendedor_id': solicitud.vendedor_id,
        'producto_id': solicitud.id_prod_sol
    }
    producto = Prod.get_one_prod(data_prod)
    relacion = Rel.get_one_rel_by_others(data_rel)
    cantidad_x_prov = producto.cantidad_x_prov
    cantidad_en_ven = producto.cantidad_en_ven
    cantidad_x_ven = relacion.cantidad_x_ven
    cantidad_sol = solicitud.cantidad_sol
    cantidad_x_prov = cantidad_x_prov
    cantidad_en_ven = cantidad_en_ven + cantidad_sol
    cantidad_x_ven = cantidad_x_ven + cantidad_sol
    data_b = {
        "cantidad_x_prov":cantidad_x_prov,
        "cantidad_en_ven": cantidad_en_ven,
        "id": solicitud.id_prod_sol,
    }
    Prod.update_prod_x_inv_total(data_b)
    data_c = {
        "cantidad_x_ven":cantidad_x_ven,
        'vendedor_id': solicitud.vendedor_id,
        'producto_id': solicitud.id_prod_sol
    }
    Rel.update_rel_x_2(data_c)
    Sol.update_sol_aceptar(data_a)
    return redirect("/proveedor/inicio")

@app.route('/denegar/solicitud/<int:id_sol>')
def denegar_solicitud(id_sol):
    data_a = {
        'id_sol': id_sol
    }
    Sol.update_sol_denegar(data_a)
    return redirect("/proveedor/inicio")