# =====================================================================
# ARCHIVO PRINCIPAL DE LA APLICACIÓN - CONDOMINIO APP
# Este archivo inicializa la aplicación Flask, configura las extensiones
# y registra todos los controladores (Blueprints).
# =====================================================================

# 1. IMPORTACIONES DE LIBRERÍAS
import os
from flask import Flask, render_template, session
from flask_mail import Mail
from whitenoise import WhiteNoise # Importar WhiteNoise

# =====================================================================
# 2. INICIALIZACIÓN Y CONFIGURACIÓN DE LA APLICACIÓN
# =====================================================================

# Creamos la instancia principal de la aplicación Flask.
# Le indicamos dónde encontrar las plantillas y los archivos estáticos.
app = Flask(__name__, template_folder='views', static_folder='views/static')

# --- Configuración General ---
# Se necesita una 'secret_key' para manejar las sesiones de usuario de forma segura.
app.secret_key = os.urandom(24)

# --- Configuración de Correo (Flask-Mail) ---
# Se obtienen las credenciales del archivo .env (que Render provee como variables de entorno).
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('Urbana Living Admin', os.environ.get('MAIL_USERNAME'))

# Inicializamos la extensión Mail con la configuración de nuestra app.
mail = Mail(app)

# --- Configuración de WhiteNoise (PARA ARCHIVOS ESTÁTICOS EN PRODUCCIÓN) ---
# "Envolvemos" nuestra aplicación con WhiteNoise. Esto es lo que soluciona el problema
# de que los CSS/JS no carguen en Render.
# WhiteNoise interceptará las peticiones a la carpeta '/static' y las servirá correctamente.
app.wsgi_app = WhiteNoise(app.wsgi_app, root='views/static/')

# =====================================================================
# 3. REGISTRO DE CONTROLADORES (BLUEPRINTS)
# =====================================================================

# Hacemos estas importaciones DESPUÉS de haber creado e inicializado 'app'.
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.inquilino_controller import inquilino_bp

# Le decimos a nuestra aplicación principal que use las rutas definidas
# en cada uno de los controladores.
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(inquilino_bp)

# =====================================================================
# 4. RUTAS PRINCIPALES (PÁGINA DE PRESENTACIÓN PÚBLICA)
# =====================================================================

@app.route('/')
def index():
    """Ruta para la página de inicio (presentación)."""
    return render_template('pages/presentacion/index.html')

@app.route('/contacto')
def contacto():
    """Ruta para la página de contacto."""
    # (Si decides crear una página de contacto, esta ruta ya está lista)
    return render_template('pages/presentacion/contacto.html')

# =====================================================================
# 5. PUNTO DE ENTRADA PARA EJECUTAR LA APLICACIÓN
# =====================================================================

# Este bloque solo se ejecuta cuando corres el comando "python app.py" en tu PC.
# Gunicorn (en Render) no usa este bloque, llama directamente a la variable 'app'.
if __name__ == '__main__':
    app.run(debug=True, port=5000)