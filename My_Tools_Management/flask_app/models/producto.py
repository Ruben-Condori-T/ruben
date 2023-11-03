from flask_app.config.mysqlconnection import connectToMySQL
import re # Biblioteca importada para el manejo de expresiones regulares
from flask_app import app
from flask import render_template,redirect,request,session,flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Prod:
    def __init__(self,data):
        self.id = data['id']
        self.nombre_prod = data['nombre_prod']
        self.precio_prod = data['precio_prod']
        self.descripcion_prod = data['descripcion_prod']
        self.img_prod = data['img_prod']
        self.cantidad_x_prov = data['cantidad_x_prov']
        self.cantidad_en_ven = data['cantidad_en_ven']
        self.created_at_prod = data['created_at_prod']
        self.updated_at_prod = data['updated_at_prod']
        self.proveedor_id = data['proveedor_id']

    #Ahora tenemos que definir para que sirve cada parte
    #Primero para crear producto
    @classmethod
    def save_prod(cls,data):
        query = "INSERT INTO productos (nombre_prod,precio_prod,descripcion_prod, img_prod,cantidad_x_prov, cantidad_en_ven, created_at_prod, updated_at_prod,proveedor_id) VALUES (%(nombre_prod)s,%(precio_prod)s,%(descripcion_prod)s,%(img_prod)s,0,0,NOW(),NOW(),%(proveedor_id)s)"
        mysql = connectToMySQL('tools')
        result = mysql.query_db(query,data) 
        data_prod = {'id': result}
        return cls.get_one_prod(data_prod)
    #################ACÁ CAMBIAREMOS EL CÓMO BUSCAMOS LA INFORMACIÓN
    @classmethod
    def get_one_prod(cls,data):
        query = "SELECT * FROM productos WHERE productos.id = %(id)s;"
        user_from_db = connectToMySQL('tools').query_db(query,data)
        return cls(user_from_db[0])
    @classmethod
    def destroy_prod(cls,data):
        query = "DELETE FROM productos WHERE id = %(id)s;"
        return connectToMySQL('tools').query_db(query,data)
    #PRUEBA
    ##A REVISARRRRRRRRRRR##
    @staticmethod
    def validate_prod_add(prod):
        is_valid = True # asumimos que esto es true
        if len(prod['new_precio']) == 0:
            flash("El precio debe de ser mayor a 0","creating")
            is_valid = False
        if int(prod['new_precio']) <=0:
            flash("El precio debe de ser mayor a 0","creating")
            is_valid = False
        if len(prod['new_nombre']) < 1:
            flash("Debe rellenar el aspecto: Nombre","creating")
            is_valid = False
        if len(prod['new_descripcion']) < 1:
            flash("Debe rellenar el aspecto: Descripcion","creating")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_prod_edit(prod):
        is_valid = True # asumimos que esto es true
        if len(prod['edit_precio']) == 0:
            flash("El precio debe de ser mayor a 0","editing")
            is_valid = False
        if len(prod['edit_nombre']) < 1:
            flash("Debe rellenar el aspecto: Nombre","editing")
            print(prod['edit_nombre'])
            is_valid = False
        if len(prod['edit_descripcion']) < 1:
            flash("Debe rellenar el aspecto: Descripcion","editing")
            is_valid = False
        return is_valid

    @classmethod
    def update_prod_x_productos(cls,data):
        query = "UPDATE productos SET nombre_prod=%(nombre_prod)s, precio_prod=%(precio_prod)s, descripcion_prod=%(descripcion_prod)s, updated_at_prod=NOW() WHERE id=%(id)s;"
        return connectToMySQL('tools').query_db(query,data)
    @classmethod
    def update_prod_x_productos_and_img(cls,data):
        query = "UPDATE productos SET nombre_prod=%(nombre_prod)s, precio_prod=%(precio_prod)s, descripcion_prod=%(descripcion_prod)s, updated_at_prod=NOW() , img_prod=%(img_prod)s WHERE id=%(id)s;"
        return connectToMySQL('tools').query_db(query,data)
    @classmethod
    def update_prod_x_inv_total(cls,data):
        query = "UPDATE productos SET cantidad_x_prov=%(cantidad_x_prov)s, cantidad_en_ven=%(cantidad_en_ven)s WHERE id=%(id)s;"
        return connectToMySQL('tools').query_db(query,data)
    @classmethod
    def destroy_prod(cls,data):
        query = "DELETE FROM productos WHERE id = %(id)s;"
        return connectToMySQL('tools').query_db(query,data)