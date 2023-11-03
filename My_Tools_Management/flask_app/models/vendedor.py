from flask_app.config.mysqlconnection import connectToMySQL
import re # Biblioteca importada para el manejo de expresiones regulares
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
from flask_app.models.producto import Prod
from flask_app.models.relacion import Rel
from flask_app.models.solicitud import Sol
import datetime
from datetime import datetime, timedelta
bcrypt = Bcrypt(app) 
#index, pestaña principal
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Ven:
    def __init__(self,data):
        self.id_ven = data['id_ven']
        self.first_name_ven = data['first_name_ven']
        self.last_name_ven = data['last_name_ven']
        self.email_ven = data['email_ven']
        self.lat_ven = data['lat_ven']
        self.lng_ven = data['lng_ven']
        self.img_ven = data['img_ven']
        self.password_ven = data['password_ven']
        self.created_at_ven = data['created_at_ven']
        self.updated_at_ven = data['updated_at_ven']
        self.proveedor_id = data['proveedor_id']
        self.prods = []
    #Ahora tenemos que definir para que sirve cada parte
    #Primero para crear usuario
    @classmethod
    def save_ven(cls,data):
        query = "INSERT INTO vendedores (first_name_ven,last_name_ven,email_ven,lat_ven,lng_ven,img_ven,password_ven,created_at_ven,updated_at_ven, proveedor_id) VALUES (%(first_name_ven)s,%(last_name_ven)s,%(email_ven)s,%(lat_ven)s,%(lng_ven)s,%(img_ven)s,%(password_ven)s,NOW(),NOW(),%(proveedor_id)s)"
        return connectToMySQL('tools').query_db(query,data)
    #Este para seleccionar el usuario registrado
    @classmethod
    def get_one_ven(cls,data):
        query = "SELECT * FROM vendedores WHERE vendedores.id_ven = %(id_ven)s;"
        user_from_db = connectToMySQL('tools').query_db(query,data)
        return cls(user_from_db[0])
    @classmethod
    def getEmail_ven(cls, email_ven):
        query = "select * from vendedores where vendedores.email_ven = %(email_ven)s;"
        data = {
            'email_ven': email_ven
        }
        result = connectToMySQL('tools').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return False
    @classmethod
    def getcodigo_prov(cls, codigo_prov):
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
    def validate_ven_reg(ven):
        is_valid = True # asumimos que esto es true
        if len(ven['first_name_ven']) < 2:
            flash("El campo First Name debe contener como mínimo 2 caracteres","register_ven")
            is_valid = False
        if len(ven['last_name_ven']) < 2:
            flash("El campo Last Name debe contener como mínimo 2 caracteres","register_ven")
            is_valid = False
        if not EMAIL_REGEX.match(ven['email_1_ven']): 
            flash("Email inválido","register_ven")
            is_valid = False
        if Ven.getEmail_ven(ven['email_1_ven']):
            flash("Correo preexistente","register_ven")
            is_valid = False
        if len(ven['codigo_prov']) != 8:
            flash("El codigo de proveedor es de 8 caracteres","register_ven")
            is_valid = False
        if not Ven.getcodigo_prov(ven['codigo_prov']):
            flash("El codigo de proveedor que proporcionó no existe en nuestra base de datos","register_ven")
            is_valid = False
        if len(ven['password_1a_ven']) < 8:
            flash("La contraseña debe contar con al menos 8 caracteres","register_ven")
            is_valid = False
        if len(ven['password_1b_ven']) < 8:
            flash("La contraseña debe contar con al menos 8 caracteres","register_ven")
            is_valid = False
        if ven['password_1a_ven'] != ven['password_1b_ven']:
            flash("Ambas contraseñas deben de ser iguales","register_ven")
            is_valid = False
        return is_valid
    #Validación del LOGIN es en el controllers
    @classmethod
    def get_prods_by_ven(cls, data):
        # Ej. data = {'idGrupo': 5}
        query = "SELECT * FROM vendedores JOIN relaciones ON vendedores.id_ven = relaciones.vendedor_id JOIN productos ON relaciones.producto_id = productos.id WHERE vendedores.id_ven = %(id_ven)s ORDER BY nombre_prod;"
        mysql = connectToMySQL('tools')
        results = mysql.query_db(query, data)
        products = []
        print('resultados 1',results)
        for result in results:
            data_prod = {
                'id': result['id']
            }
            data_rel = {
                'id_rel': result['id_rel']
            }
            products.append({
                'id': Prod.get_one_prod(data_prod).id,
                'nombre_prod': Prod.get_one_prod(data_prod).nombre_prod,
                'precio_prod': Prod.get_one_prod(data_prod).precio_prod,
                'descripcion_prod': Prod.get_one_prod(data_prod).descripcion_prod,
                'img_prod': Prod.get_one_prod(data_prod).img_prod,
                'cantidad_x_prov': Prod.get_one_prod(data_prod).cantidad_x_prov,
                'cantidad_en_ven': Prod.get_one_prod(data_prod).cantidad_en_ven,
                'cantidad_x_ven': Rel.get_one_rel(data_rel).cantidad_x_ven,
                'relacion_id': Rel.get_one_rel(data_rel).id_rel,
                'created_at_prod': Prod.get_one_prod(data_prod).created_at_prod,
                'updated_at_prod': Prod.get_one_prod(data_prod).updated_at_prod,
                });
        print("gol",products)
        return products
    @classmethod
    def get_one_ven(cls,data):
        query = "SELECT * FROM vendedores WHERE vendedores.id_ven = %(id_ven)s;"
        user_from_db = connectToMySQL('tools').query_db(query,data)
        return cls(user_from_db[0])
    
    @classmethod
    def get_sols_by_ven(cls, data):
        # Ej. data = {'idGrupo': 5}
        query = "SELECT * FROM vendedores JOIN solicitudes ON vendedores.id_ven = solicitudes.vendedor_id JOIN proveedores ON solicitudes.proveedor_id = proveedores.id_prov JOIN productos ON proveedores.id_prov = productos.proveedor_id JOIN relaciones ON productos.id = relaciones.producto_id WHERE id_ven = %(id_ven)s AND id_ven = relaciones.vendedor_id AND id_prod_sol = productos.id ORDER BY created_at_sol DESC;"
        mysql = connectToMySQL('tools')
        results = mysql.query_db(query, data)
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
            x = Sol.get_one_sol(data_sol).updated_at_sol
            print(x)
            fecha_hoy = datetime.now()
            dia_hoy = fecha_hoy.day
            mes_hoy = fecha_hoy.month
            año_hoy = fecha_hoy.year
            y = datetime(año_hoy, mes_hoy, dia_hoy)
            z = y-x
            h = z.days
            print(h)
            if h < 2:
                tiempo_sol = 0
            else:
                tiempo_sol = 1
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
                'nombre_prod_sol': Prod.get_one_prod(data_prod).nombre_prod,
                'cantidad_x_ven': Rel.get_one_rel(data_rel).cantidad_x_ven,
                'first_name_ven': Ven.get_one_ven(data_ven).first_name_ven,
                'last_name_ven': Ven.get_one_ven(data_ven).last_name_ven,
                'tiempo_sol': tiempo_sol,
                });
        print("gol",solicitudes)
        return solicitudes