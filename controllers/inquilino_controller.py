from flask import Blueprint, render_template

# Aquí definimos la variable 'inquilino_bp'.
# Este Blueprint gestionará el portal personal de cada inquilino.
inquilino_bp = Blueprint(
    'inquilino', __name__,
    url_prefix='/inquilino', # Todas las rutas aquí empezarán con /inquilino
    template_folder='../views'
)

@inquilino_bp.route('/cuenta')
def mi_cuenta():
    """Ruta para la página principal de la cuenta del inquilino."""
    return render_template('pages/inquilino/mi_cuenta.html')

@inquilino_bp.route('/pagos')
def mis_pagos():
    """Ruta para ver el historial de pagos del inquilino."""
    return render_template('pages/inquilino/mis_pagos.html')


from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from models.inquilino_model import get_inquilino_por_id
from models.habitacion_model import get_habitacion_por_inquilino_id
from models.pago_model import get_pagos_por_inquilino
from models.calendario_model import get_eventos_inquilino

inquilino_bp = Blueprint('inquilino', __name__, url_prefix='/inquilino')

# --- Middleware de seguridad para proteger todas las rutas de este blueprint ---
@inquilino_bp.before_request
def verificar_sesion_inquilino():
    if 'user_role' not in session or session['user_role'] != 'inquilino':
        return redirect(url_for('auth.login'))

# --- RUTAS DEL PORTAL ---

@inquilino_bp.route('/cuenta')
def mi_cuenta():
    id_inquilino_actual = session['user_id']
    inquilino = get_inquilino_por_id(id_inquilino_actual)
    habitacion = get_habitacion_por_inquilino_id(id_inquilino_actual)
    
    return render_template('pages/inquilino/mi_cuenta.html', inquilino=inquilino, habitacion=habitacion)

@inquilino_bp.route('/pagos')
def mis_pagos():
    id_inquilino_actual = session['user_id']
    pagos = get_pagos_por_inquilino(id_inquilino_actual)
    return render_template('pages/inquilino/mis_pagos.html', pagos=pagos)

# --- RUTA API PARA EL CALENDARIO ---
@inquilino_bp.route('/api/mis_eventos')
def api_mis_eventos():
    id_inquilino_actual = session['user_id']
    eventos = get_eventos_inquilino(id_inquilino_actual)
    return jsonify(eventos)