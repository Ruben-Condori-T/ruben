from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.producto import Prod
from flask_app.models.relacion import Rel
from flask_app.models.vendedor import Ven
from flask_app.models.proveedor import Prov
from flask_app.models.solicitud import Sol
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/prov')
def prov():
    return redirect('/proveedor')
@app.route('/ven')
def ven():
    return redirect('/vendedor')
@app.route("/logout/proveedor")
def home_prov():
    session.clear()
    return redirect("/")
@app.route("/logout/vendedor")
def home_ven():
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
    session.clear()
    return redirect("/")
#Intento
