from flask_app.config.mysqlconnection import connectToMySQL
import re # Biblioteca importada para el manejo de expresiones regulares
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.producto import Prod
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Sol:
    def __init__(self,data):
        self.id_sol = data['id_sol']
        self.cantidad_sol = data['cantidad_sol']
        self.id_prod_sol = data['id_prod_sol']
        self.razon_sol = data['razon_sol']
        self.estado_sol = data['estado_sol']
        self.created_at_sol = data['created_at_sol']
        self.updated_at_sol = data['updated_at_sol']
        self.proveedor_id = data['proveedor_id']
        self.vendedor_id = data['vendedor_id']

    #Ahora tenemos que definir para que sirve cada parte
    #Primero para crear producto
    @classmethod
    def save_sol(cls,data):
        query = "INSERT INTO solicitudes (cantidad_sol, id_prod_sol,razon_sol,estado_sol,created_at_sol, updated_at_sol,proveedor_id,vendedor_id) VALUES (%(cantidad_sol)s,%(id_prod_sol)s,%(razon_sol)s,0,NOW(),NOW(),%(proveedor_id)s,%(vendedor_id)s)"
        return connectToMySQL('tools').query_db(query,data)
    
    #################ACÁ CAMBIAREMOS EL CÓMO BUSCAMOS LA INFORMACIÓN
    @classmethod
    def get_one_sol(cls,data):
        query = "SELECT * FROM solicitudes WHERE solicitudes.id_sol = %(id_sol)s;"
        user_from_db = connectToMySQL('tools').query_db(query,data)
        return cls(user_from_db[0])
    @classmethod
    def get_rels_by_prov(cls,data):
        query = "SELECT * FROM solicitudes WHERE solicitudes.proveedor_id = %(proveedor_id)s;"
        user_from_db = connectToMySQL('tools').query_db(query,data)
        return cls(user_from_db[0])
    
    @classmethod
    def get_rels_by_ven(cls,data):
        query = "SELECT * FROM solicitudes WHERE solicitudes.vendedor_id = %(vendedor_id)s;"
        user_from_db = connectToMySQL('tools').query_db(query,data)
        return cls(user_from_db[0])
    @classmethod
    def destroy_one_sol(cls,data):
        query = "DELETE FROM solicitudes WHERE id_sol = %(id_sol)s;"
        return connectToMySQL('tools').query_db(query,data)
    @classmethod
    def destroy_sol_by_prod(cls,data):
        query = "DELETE FROM solicitudes WHERE solicitudes.id_prod_sol = %(id_prod_sol)s;"
        return connectToMySQL('tools').query_db(query,data)
    @classmethod
    def destroy_sol_by_prov(cls,data):
        query = "DELETE FROM solicitudes WHERE solicitudes.proveedor_id = %(proveedor_id)s;"
        return connectToMySQL('tools').query_db(query,data)
    @classmethod
    def destroy_sol_by_ven(cls,data):
        query = "DELETE FROM solicitudes WHERE solicitudes.vendedor_id = %(vendedor_id)s;"
        return connectToMySQL('tools').query_db(query,data)
    
    #PRUEBA
    ##A REVISARRRRRRRRRRR##

    @classmethod
    def update_sol_aceptar(cls,data):
        query = "UPDATE solicitudes SET estado_sol=1, updated_at_sol=NOW() WHERE id_sol=%(id_sol)s;"
        return connectToMySQL('tools').query_db(query,data)
    @classmethod
    def update_sol_denegar(cls,data):
        query = "UPDATE solicitudes SET estado_sol=2, updated_at_sol=NOW() WHERE id_sol=%(id_sol)s;"
        return connectToMySQL('tools').query_db(query,data)
    