from flask_app.config.mysqlconnection import connectToMySQL
import re # Biblioteca importada para el manejo de expresiones regulares
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.producto import Prod
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Rel:
    def __init__(self,data):
        self.id_rel = data['id_rel']
        self.cantidad_x_ven = data['cantidad_x_ven']
        self.created_at_rel = data['created_at_rel']
        self.updated_at_rel = data['updated_at_rel']
        self.producto_id = data['producto_id']
        self.vendedor_id = data['vendedor_id']

    #Ahora tenemos que definir para que sirve cada parte
    #Primero para crear producto
    @classmethod
    def save_rel(cls,data):
        query = "INSERT INTO relaciones (cantidad_x_ven, created_at_rel, updated_at_rel,producto_id,vendedor_id) VALUES (0,NOW(),NOW(),%(producto_id)s,%(vendedor_id)s)"
        return connectToMySQL('tools').query_db(query,data)
    
    #################ACÁ CAMBIAREMOS EL CÓMO BUSCAMOS LA INFORMACIÓN
    @classmethod
    def get_one_rel(cls,data):
        query = "SELECT * FROM relaciones WHERE relaciones.id_rel = %(id_rel)s;"
        user_from_db = connectToMySQL('tools').query_db(query,data)
        return cls(user_from_db[0])
    @classmethod
    def get_one_rel_by_others(cls,data):
        query = "SELECT * FROM relaciones WHERE relaciones.producto_id = %(producto_id)s AND relaciones.vendedor_id = %(vendedor_id)s;"
        user_from_db = connectToMySQL('tools').query_db(query,data)
        return cls(user_from_db[0])
    @classmethod
    def get_rels_by_prod(cls,data):
        query = "SELECT * FROM relaciones WHERE relaciones.producto_id = %(producto_id)s;"
        user_from_db = connectToMySQL('tools').query_db(query,data)
        return cls(user_from_db[0])
    
    @classmethod
    def destroy_one_rel(cls,data):
        query = "DELETE FROM relaciones WHERE id_rel = %(id_rel)s;"
        return connectToMySQL('tools').query_db(query,data)
    
    @classmethod
    def destroy_rels_by_prod(cls,data):
        query = "DELETE FROM relaciones WHERE relaciones.producto_id = %(producto_id)s;"
        return connectToMySQL('tools').query_db(query,data)
    #PRUEBA
    ##A REVISARRRRRRRRRRR##

    @classmethod
    def update_rel_x_1(cls,data):
        query = "UPDATE relaciones SET cantidad_x_ven=%(cantidad_x_ven)s, updated_at_rel=NOW() WHERE id_rel=%(id_rel)s;"
        return connectToMySQL('tools').query_db(query,data)

    @classmethod
    def update_rel_x_2(cls,data):
        query = "UPDATE relaciones SET cantidad_x_ven=%(cantidad_x_ven)s, updated_at_rel=NOW() WHERE producto_id=%(producto_id)s AND vendedor_id=%(vendedor_id)s;"
        return connectToMySQL('tools').query_db(query,data)