#Todo lo relacionado a gestión de inventarios de proveedores y reporte diario de vendedor

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

#Gestión de inventarios de proveedores
@app.route('/proveedor/inventario/actualizar/prov/<int:prov_id>',methods=['POST'])
def actualizar_inventario(prov_id):
    if request.method == 'POST':
        data_a = {
            'id_prov': prov_id,
        }
        is_Valid = False
        validez = 0
        ids_prods = []
        print(Prov.get_prods_by_prov(data_a))
        for i in Prov.get_prods_by_prov(data_a):
            print("Se imprime lo siguiente:           ",i['id'])
            ids_prods.append(i['id'])
        for num in ids_prods:
            pedido_1 = "entrada_" + str(num)
            pedido_2 = "merma_" + str(num)
            entrante = int(request.form[pedido_1])
            merma = int(request.form[pedido_2])
            data = {
            'id': num,
            }
            producto = Prod.get_one_prod(data)
            cantidad_x_prov = int(producto.cantidad_x_prov)
            cantidad_en_ven = int(producto.cantidad_en_ven)
            if (cantidad_x_prov - cantidad_en_ven + entrante - merma)<0 :
                mensaje = "Verificar el balance que desea añadir en " + str(producto.nombre_prod)
                flash(mensaje,"actualizar_prov")
                validez=validez+1
        if validez == 0 :
            is_Valid = True
        if is_Valid:
            for num in ids_prods:
                pedido_1 = "entrada_" + str(num)
                pedido_2 = "merma_" + str(num)
                entrante = int(request.form[pedido_1])
                merma = int(request.form[pedido_2])
                data = {
                'id': int(num),
                }
                producto = Prod.get_one_prod(data)
                cantidad_x_prov = int(producto.cantidad_x_prov)
                cantidad_en_ven = int(producto.cantidad_en_ven)
                cantidad_x_prov = cantidad_x_prov + entrante - merma
                cantidad_en_ven = cantidad_en_ven
                print("ahora la cantidad será", cantidad_x_prov)
                data_b = {
                    'cantidad_x_prov': cantidad_x_prov,
                    'cantidad_en_ven':cantidad_en_ven,
                    'id': num,
                }
                Prod.update_prod_x_inv_total(data_b)
        return redirect('/proveedor/inventario')
@app.route('/proveedor/inventario/<int:id_ven>')
def proveedor_inventario_x_vendedor(id_ven):
    data_b = {
        "id_ven": id_ven,
    }
    return render_template("inventario_prov_ven.html",all_prods=Ven.get_prods_by_ven(data_b), ven=Ven.get_one_ven(data_b))

#Gestión de inventario del vendedor por parte del proveedor
@app.route('/proveedor/inventario/actualizar/ven/<int:ven_id>',methods=['POST'])
def actualizar_inventario_x_vendedor(ven_id):
    if request.method == 'POST':
        data_a = {
            'id_ven' : ven_id,
        }
        vendedor = Ven.get_one_ven(data_a)
        is_Valid = False
        validez = 0
        ids_prods = []
        print(Ven.get_prods_by_ven(data_a))
        for i in Ven.get_prods_by_ven(data_a):
            print("AHORA", i)
            pedido_1 = "entrada_" + str(i['id'])
            pedido_2 = "venta_" + str(i['id'])
            entrante = int(request.form[pedido_1])
            merma = int(request.form[pedido_2])
            cantidad_en_ven = int(i['cantidad_en_ven'])
            cantidad_x_ven = int(i['cantidad_x_ven'])
            if (cantidad_x_ven  + entrante - merma)<0 :
                mensaje = "Verificar el balance que desea añadir en " + str(id['nombre_prod'])
                flash(mensaje,"actualizar_prov_ven")
                validez=validez+1
        if validez == 0 :
            is_Valid = True
        if is_Valid:
            for i in Ven.get_prods_by_ven(data_a):
                print("AHORITA MISMO", int(i['cantidad_en_ven']))
                pedido_1 = "entrada_" + str(i['id'])
                pedido_2 = "venta_" + str(i['id'])
                entrante = int(request.form[pedido_1])
                merma = int(request.form[pedido_2])
                data_b = {
                    'id': int(i['id']),
                }
                producto = Prod.get_one_prod(data_b)

                cantidad_x_prov = int(i['cantidad_x_prov'])
                cantidad_en_ven = int(i['cantidad_en_ven'])
                cantidad_x_ven = int(i['cantidad_x_ven'])

                cantidad_x_prov = cantidad_x_prov - merma
                cantidad_en_ven = cantidad_en_ven + entrante - merma
                cantidad_x_ven = cantidad_x_ven + entrante - merma
                print("ahora la cantidad será", cantidad_x_ven)
                data_c = {
                    'cantidad_x_prov': cantidad_x_prov,
                    'cantidad_en_ven':cantidad_en_ven,
                    'id': int(i['id']),
                }
                data_d = {
                    'cantidad_x_ven': cantidad_x_ven,
                    'id_rel' : int(i['relacion_id']),
                }
                Prod.update_prod_x_inv_total(data_c)
                Rel.update_rel_x_1(data_d)
        link = "/proveedor/inventario/"+ str(ven_id)
        return redirect(link)
#Inventario desde el lado del vendedor (Revisión)
@app.route('/vendedor/inventario')
def vendedor_inventario():
    data = {
        "id_ven": session["user_id"],
    }
    return render_template("inventario_ven.html",all_prods=Ven.get_prods_by_ven(data))

@app.route('/vendedor/inventario/<int:prod_id>')
def ver_inventario_prod(prod_id):
    if 'key_name' in session:
        data_a = {
            'id': prod_id,
        }
        producto = Prod.get_one_prod(data_a)
        print("pikapi",producto)
        return render_template("view_ven.html",prod=producto)
    else:
        return redirect('/')

#Reporte de venta
@app.route('/vendedor/reporte')
def vendedor_reporte():
    data_b = {
        "id_ven": session['user_id'],
    }
    return render_template("report_ven.html",all_prods=Ven.get_prods_by_ven(data_b), ven=Ven.get_one_ven(data_b))



@app.route('/vendedor/reporte/actualizar/<int:ven_id>',methods=['POST'])
def actualizar_vendedor(ven_id):
    if request.method == 'POST':
        data_a = {
            'id_ven' : ven_id,
        }
        vendedor = Ven.get_one_ven(data_a)
        is_Valid = False
        validez = 0
        ids_prods = []
        print(Ven.get_prods_by_ven(data_a))
        for i in Ven.get_prods_by_ven(data_a):
            print("AHORA", i)
            pedido_2 = "venta_" + str(i['id'])
            venta = int(request.form[pedido_2])
            cantidad_en_ven = int(i['cantidad_en_ven'])
            cantidad_x_ven = int(i['cantidad_x_ven'])
            if (cantidad_x_ven - venta)<0 :
                mensaje = "Verificar si se excedió al indicar la venta de " + str(id['nombre_prod'])
                flash(mensaje,"actualizar_prov_ven")
                validez=validez+1
        if validez == 0 :
            is_Valid = True
        if is_Valid:
            for i in Ven.get_prods_by_ven(data_a):
                print("AHORITA MISMO", int(i['cantidad_en_ven']))
                pedido_2 = "venta_" + str(i['id'])
                venta = int(request.form[pedido_2])
                data_b = {
                    'id': int(i['id']),
                }
                producto = Prod.get_one_prod(data_b)

                cantidad_x_prov = int(i['cantidad_x_prov'])
                cantidad_en_ven = int(i['cantidad_en_ven'])
                cantidad_x_ven = int(i['cantidad_x_ven'])

                cantidad_x_prov = cantidad_x_prov - venta
                cantidad_en_ven = cantidad_en_ven - venta
                cantidad_x_ven = cantidad_x_ven - venta
                print("ahora la cantidad será", cantidad_x_ven)
                data_c = {
                    'cantidad_x_prov': cantidad_x_prov,
                    'cantidad_en_ven':cantidad_en_ven,
                    'id': int(i['id']),
                }
                data_d = {
                    'cantidad_x_ven': cantidad_x_ven,
                    'id_rel' : int(i['relacion_id']),
                }
                Prod.update_prod_x_inv_total(data_c)
                Rel.update_rel_x_1(data_d)
        link = "/vendedor/inicio"
        return redirect(link)