from flask_app import app
# ...server.py

from flask_app.controllers import productos
from flask_app.controllers import vendedores
from flask_app.controllers import proveedores
from flask_app.controllers import general
from flask_app.controllers import inventarios
from flask_app.controllers import solicitudes
# ...server.py

if __name__=="__main__":
    app.run(debug=True)