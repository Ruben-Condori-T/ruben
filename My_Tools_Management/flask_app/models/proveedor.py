from flask_app.config.mysqlconnection import connectToMySQL
import re # Biblioteca importada para el manejo de expresiones regulares
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
from flask_app.models.producto import Prod
from flask_app.models.relacion import Rel
from flask_app.models.vendedor import Ven
from flask_app.models.solicitud import Sol
from datetime import datetime, timedelta
bcrypt = Bcrypt(app) 
#index, pestaña principal
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Prov:
    def __init__(self,data):
        self.id_prov = data['id_prov']
        self.first_name_prov = data['first_name_prov']
        self.last_name_prov = data['last_name_prov']
        self.email_prov = data['email_prov']
        self.lat_prov = data['lat_prov']
        self.lng_prov = data['lng_prov']
        self.img_prov = data['img_prov']
        self.password_prov = data['password_prov']
        self.codigo_prov = data['codigo_prov']
        self.created_at_prov = data['created_at_prov']
        self.updated_at_prov = data['updated_at_prov']
    #Ahora tenemos que definir para que sirve cada parte
    #Primero para crear usuario
    @classmethod
    def save_prov(cls,data):
        query = "INSERT INTO proveedores (first_name_prov,last_name_prov,email_prov,lat_prov,lng_prov,img_prov,password_prov,codigo_prov,created_at_prov,updated_at_prov) VALUES (%(first_name_prov)s,%(last_name_prov)s,%(email_prov)s,%(lat_prov)s,%(lat_prov)s,%(img_prov)s,%(password_prov)s,%(codigo_prov)s,NOW(),NOW())"
        return connectToMySQL('tools').query_db(query,data)
    #Este para seleccionar el usuario registrado
    @classmethod
    def get_one_prov(cls,data):
        query = "SELECT * FROM proveedores WHERE proveedores.id_prov = %(id_prov)s;"
        user_from_db = connectToMySQL('tools').query_db(query,data)
        return cls(user_from_db[0])
    @classmethod
    def getEmail_prov(cls, email_prov):
        query = "select * from proveedores where proveedores.email_prov = %(email_prov)s;"
        data = {
            'email_prov': email_prov
        }
        result = connectToMySQL('tools').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return False
    #TODAVÍA A DESARROLLARSE
    @classmethod
    def generatecodigo_prov(cls, codigo_prov):
        query = "select * from proveedores where proveedores.codigo_prov = %(codigo_prov)s;"
        data = {
            'codigo_prov': codigo_prov
        }
        result = connectToMySQL('tools').query_db(query, data)
        if len(result) > 0:
            return True
        else:
            return False
    @staticmethod
    def validate_prov_reg(prov):
        is_valid = True # asumimos que esto es true
        if len(prov['first_name_prov']) < 2:
            flash("El campo First Name debe contener como mínimo 2 caracteres","register_prov")
            is_valid = False
        if len(prov['last_name_prov']) < 2:
            flash("El campo Last Name debe contener como mínimo 2 caracteres","register_prov")
            is_valid = False
        if not EMAIL_REGEX.match(prov['email_1_prov']): 
            flash("Email inválido","register_prov")
            is_valid = False
        if Prov.getEmail_prov(prov['email_1_prov']):
            flash("Correo preexistente","register_prov")
            is_valid = False
        if len(prov['password_1a_prov']) < 8:
            flash("La contraseña debe contar con al menos 8 caracteres","register_prov")
            is_valid = False
        if len(prov['password_1b_prov']) < 8:
            flash("La contraseña debe contar con al menos 8 caracteres","register_prov")
            is_valid = False
        if prov['password_1a_prov'] != prov['password_1b_prov']:
            flash("Ambas contraseñas deben de ser iguales","register_prov")
            is_valid = False
        return is_valid
    #Validación del LOGIN es en el controllers
    @classmethod
    def get_prods_by_prov(cls, data):
        # Ej. data = {'idGrupo': 5}
        query = "SELECT * FROM proveedores JOIN productos ON proveedores.id_prov = productos.proveedor_id WHERE id_prov = %(id_prov)s ORDER BY nombre_prod;"
        mysql = connectToMySQL('tools')
        results = mysql.query_db(query, data)
        productos_total = []
        print('resultados 2',results)
        for result in results:
            data_prod = {
                'id': result['id']
            }
            productos_total.append({
                'id': Prod.get_one_prod(data_prod).id,
                'nombre_prod': Prod.get_one_prod(data_prod).nombre_prod,
                'precio_prod': Prod.get_one_prod(data_prod).precio_prod,
                'descripcion_prod': Prod.get_one_prod(data_prod).descripcion_prod,
                'img_prod': Prod.get_one_prod(data_prod).img_prod,
                'cantidad_x_prov': Prod.get_one_prod(data_prod).cantidad_x_prov,
                'cantidad_en_ven': Prod.get_one_prod(data_prod).cantidad_en_ven,
                'created_at_prod': Prod.get_one_prod(data_prod).created_at_prod,
                'updated_at_prod': Prod.get_one_prod(data_prod).updated_at_prod,
                });
        print("gol",productos_total)
        return productos_total
    @classmethod
    def get_vens_by_prov(cls, data):
        # Ej. data = {'idGrupo': 5}
        query = "SELECT * FROM proveedores JOIN vendedores ON proveedores.id_prov = vendedores.proveedor_id WHERE proveedores.id_prov = %(id_prov)s ORDER BY vendedores.first_name_ven;"
        mysql = connectToMySQL('tools')
        results = mysql.query_db(query, data)
        vendedores = []
        print('resultados',results)
        for result in results:
            data_ven = {
                'id_ven': result['id_ven']
            }
            vendedores.append({
                'id_ven': Ven.get_one_ven(data_ven).id_ven,
                'first_name_ven': Ven.get_one_ven(data_ven).first_name_ven,
                'last_name_ven': Ven.get_one_ven(data_ven).last_name_ven,
                'email_ven': Ven.get_one_ven(data_ven).email_ven,
                'lat_ven': Ven.get_one_ven(data_ven).lat_ven,
                'lng_ven': Ven.get_one_ven(data_ven).lng_ven,
                'img_ven': Ven.get_one_ven(data_ven).img_ven,
                'created_at_ven': Ven.get_one_ven(data_ven).created_at_ven,
                'updated_at_ven': Ven.get_one_ven(data_ven).updated_at_ven,
                });
        print("gol",vendedores)
        return vendedores
    @classmethod
    def get_one_prov(cls,data):
        query = "SELECT * FROM proveedores WHERE proveedores.id_prov = %(id_prov)s;"
        user_from_db = connectToMySQL('tools').query_db(query,data)
        return cls(user_from_db[0])
    @classmethod
    def get_by_codigo(cls, codigo_prov):
        query = "select * from proveedores where proveedores.codigo_prov = %(codigo_prov)s;"
        data = {
            'codigo_prov': codigo_prov
        }
        result = connectToMySQL('tools').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return False
    
    @classmethod
    def get_sols_by_prov(cls, data):
        # Ej. data = {'idGrupo': 5}
        query = "SELECT * FROM proveedores JOIN solicitudes ON proveedores.id_prov = solicitudes.proveedor_id JOIN vendedores ON solicitudes.vendedor_id = vendedores.id_ven JOIN relaciones ON vendedores.id_ven = relaciones.vendedor_id JOIN productos ON relaciones.producto_id = productos.id WHERE id_prov = %(id_prov)s AND id_ven = relaciones.vendedor_id AND id_prod_sol = productos.id ORDER BY updated_at_sol DESC;"
        mysql = connectToMySQL('tools')
        results = mysql.query_db(query, data)
        print(results)
        solicitudes = []
        print('resultados 1',results)
        for result in results:
            data_sol = {
                'id_sol': result['id_sol']
            }
            data_prod = {
                'id': result['id_prod_sol']
            }
            data_rel = {
                'id_rel': result['id_rel']
            }
            data_ven = {
                'id_ven': result['id_ven']
            }
            solicitudes.append({
                'id_sol': Sol.get_one_sol(data_sol).id_sol,
                'cantidad_sol': Sol.get_one_sol(data_sol).cantidad_sol,
                'id_prod_sol': Sol.get_one_sol(data_sol).id_prod_sol,
                'razon_sol': Sol.get_one_sol(data_sol).razon_sol,
                'estado_sol': Sol.get_one_sol(data_sol).estado_sol,
                'proveedor_id': Sol.get_one_sol(data_sol).proveedor_id,
                'vendedor_id': Sol.get_one_sol(data_sol).vendedor_id,
                'created_at_sol': Sol.get_one_sol(data_sol).created_at_sol,
                'updated_at_sol': Sol.get_one_sol(data_sol).updated_at_sol,
                'cantidad_x_prov': Prod.get_one_prod(data_prod).cantidad_x_prov,
                'cantidad_en_ven': Prod.get_one_prod(data_prod).cantidad_en_ven,
                'nombre_prod': Prod.get_one_prod(data_prod).nombre_prod,
                'cantidad_x_ven': Rel.get_one_rel(data_rel).cantidad_x_ven,
                'first_name_ven': Ven.get_one_ven(data_ven).first_name_ven,
                'last_name_ven': Ven.get_one_ven(data_ven).last_name_ven,
                })
        print("gol",solicitudes)
        return solicitudes