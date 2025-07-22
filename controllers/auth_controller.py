from flask import Blueprint, request, jsonify, session, flash, redirect, url_for
from models.user_model import verificar_credenciales

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ESTA RUTA NUEVA MANEJA EL LOGIN DEL MODAL
@auth_bp.route('/login_ajax', methods=['POST'])
def login_ajax():
    # Obtenemos los datos que envió el JavaScript en formato JSON
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email y contraseña son requeridos.'}), 400

    resultado = verificar_credenciales(email, password)

    if resultado['status'] == 'success':
        # Guardamos datos en la sesión
        session['user_id'] = resultado['data']['id']
        session['user_name'] = resultado['data']['nombres']
        session['user_role'] = resultado['role']

        # Determinamos a dónde redirigir
        if resultado['role'] == 'admin':
            redirect_url = url_for('admin.dashboard')
        else:
            redirect_url = url_for('inquilino.mi_cuenta')
        
        # Enviamos una respuesta JSON exitosa
        return jsonify({'status': 'success', 'redirect_url': redirect_url})
    else:
        # Enviamos una respuesta JSON de error
        return jsonify({'status': 'error', 'message': resultado['message']}), 401


# LA RUTA DE LOGOUT SIGUE SIENDO ÚTIL
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info') # Este flash ya no se verá, pero lo dejamos por si acaso
    return redirect(url_for('index'))

# Ya no necesitamos la ruta que mostraba la página de login, puedes borrarla.