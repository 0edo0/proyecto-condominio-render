# ---------------------------------------------------------------------
# ARCHIVO PRINCIPAL DE LA APLICACIÓN - CONDOMINIO APP
# Ejecuta este archivo para iniciar el servidor.
# ---------------------------------------------------------------------

# 1. IMPORTACIONES NECESARIAS DE FLASK
from flask import Flask, render_template
import os

# 2. CREACIÓN DE LA APLICACIÓN FLASK
# Creamos la instancia principal de la aplicación aquí mismo.
# Esta variable 'app' será importada por otros módulos si es necesario.
app = Flask(__name__, template_folder='views', static_folder='views/static')

# 3. CONFIGURACIÓN DE LA APLICACIÓN
# Es vital tener una 'secret_key' para que las sesiones de usuario funcionen.
app.secret_key = os.urandom(24)

# 4. IMPORTACIÓN DE LOS CONTROLADORES (BLUEPRINTS)
# ¡IMPORTANTE! Hacemos estas importaciones DESPUÉS de haber creado la variable 'app'.
# Esto evita el 99% de los errores de importación circular.
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.inquilino_controller import inquilino_bp

# 5. REGISTRO DE LOS BLUEPRINTS EN LA APLICACIÓN
# Le decimos a nuestra aplicación principal 'app' que use las rutas
# definidas en cada uno de los controladores.
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(inquilino_bp)

# 6. DEFINICIÓN DE RUTAS PRINCIPALES (Página de Presentación)
# Estas son las rutas que no pertenecen a "admin" o "inquilino".
@app.route('/')
def index():
    """Ruta para la página de inicio."""
    return render_template('pages/presentacion/index.html')

@app.route('/contacto')
def contacto():
    """Ruta para la página de contacto."""
    return render_template('pages/presentacion/contacto.html')

# 7. PUNTO DE ENTRADA PARA EJECUTAR LA APLICACIÓN
# Este bloque solo se ejecuta cuando corres el comando "python app.py".
if __name__ == '__main__':
    # debug=True hace que el servidor se reinicie solo cada vez que guardas un cambio.
    # Quítalo cuando la aplicación esté terminada (en producción).
    app.run(debug=True, port=5000)