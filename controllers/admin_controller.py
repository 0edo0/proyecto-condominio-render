from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from flask import request, flash
from models.calendario_model import get_eventos_admin # Importamos la nueva función
from models.habitacion_model import get_todas_las_habitaciones, get_habitacion_por_id, crear_habitacion, actualizar_habitacion, eliminar_habitacion
from models.inquilino_model import get_inquilinos_disponibles
# Asegúrate de importar los nuevos modelos de habitación
from models.habitacion_model import asignar_inquilino_a_habitacion, finalizar_alquiler
from models.inquilino_model import get_todos_los_inquilinos, get_inquilino_por_id, crear_inquilino, actualizar_inquilino, eliminar_inquilino
from models.pago_model import registrar_pago, get_pagos_por_inquilino

# ... (importaciones existentes) ...
from models.admin_model import get_todos_los_admins, get_admin_por_id, crear_admin, actualizar_admin, eliminar_admin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    """Muestra el dashboard del administrador, ahora protegido."""
    # Verificación de seguridad: solo admins pueden ver esto.
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login')) # O a una página de "no autorizado"
    
    return render_template('pages/admin/dashboard.html')

# --- NUEVA RUTA API PARA EL CALENDARIO ---
@admin_bp.route('/api/eventos_calendario')
def eventos_calendario():
    """Devuelve los eventos en formato JSON para FullCalendar."""
    # Verificación de seguridad
    if 'user_role' not in session or session['user_role'] != 'admin':
        return jsonify({"error": "No autorizado"}), 403

    eventos = get_eventos_admin()
    return jsonify(eventos)

# Aquí irán las otras rutas de gestión...

@admin_bp.route('/habitaciones')
def gestionar_habitaciones():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    habitaciones = get_todas_las_habitaciones()
    return render_template('pages/admin/gestionar_habitaciones.html', habitaciones=habitaciones)

@admin_bp.route('/habitaciones/nueva')
def form_nueva_habitacion():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    return render_template('pages/admin/form_habitacion.html', habitacion=None)

@admin_bp.route('/habitaciones/editar/<int:id_habitacion>')
def form_editar_habitacion(id_habitacion):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    habitacion = get_habitacion_por_id(id_habitacion)
    return render_template('pages/admin/form_habitacion.html', habitacion=habitacion)

@admin_bp.route('/habitaciones/procesar', methods=['POST'])
def procesar_habitacion():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    datos = request.form.to_dict()
    if 'id_habitacion' in datos and datos['id_habitacion']:
        # Es una actualización
        actualizar_habitacion(datos)
        flash('¡Habitación actualizada exitosamente!', 'success')
    else:
        # Es una creación
        crear_habitacion(datos)
        flash('¡Habitación creada exitosamente!', 'success')
    
    return redirect(url_for('admin.gestionar_habitaciones'))

@admin_bp.route('/habitaciones/eliminar/<int:id_habitacion>', methods=['POST'])
def eliminar_habitacion_route(id_habitacion):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    resultado = eliminar_habitacion(id_habitacion)
    flash(resultado['message'], resultado['status'])
    
    return redirect(url_for('admin.gestionar_habitaciones'))

# --- NUEVA RUTA API PARA OBTENER INQUILINOS ---
@admin_bp.route('/api/inquilinos_disponibles')
def api_inquilinos_disponibles():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return jsonify({"error": "No autorizado"}), 403
    
    inquilinos = get_inquilinos_disponibles()
    return jsonify(inquilinos)

# --- RUTAS PARA EL PROCESO DE ALQUILER ---
@admin_bp.route('/habitaciones/alquilar', methods=['POST'])
def alquilar_habitacion():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))

    id_habitacion = request.form['id_habitacion']
    id_inquilino = request.form['id_inquilino']
    
    resultado = asignar_inquilino_a_habitacion(id_habitacion, id_inquilino)
    flash(resultado['message'], resultado['status'])
    
    return redirect(url_for('admin.gestionar_habitaciones'))

@admin_bp.route('/habitaciones/finalizar_alquiler/<int:id_habitacion>', methods=['POST'])
def finalizar_alquiler_route(id_habitacion):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))

    resultado = finalizar_alquiler(id_habitacion)
    flash(resultado['message'], resultado['status'])
    
    return redirect(url_for('admin.gestionar_habitaciones'))




# ... (rutas de dashboard y habitaciones existentes) ...

# --- RUTAS PARA GESTIÓN DE INQUILINOS ---

@admin_bp.route('/inquilinos')
def gestionar_inquilinos():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    inquilinos = get_todos_los_inquilinos()
    return render_template('pages/admin/gestionar_inquilinos.html', inquilinos=inquilinos)

@admin_bp.route('/inquilinos/nuevo')
def form_nuevo_inquilino():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    return render_template('pages/admin/form_inquilino.html', inquilino=None)

@admin_bp.route('/inquilinos/editar/<int:id_inquilino>')
def form_editar_inquilino(id_inquilino):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    inquilino = get_inquilino_por_id(id_inquilino)
    return render_template('pages/admin/form_inquilino.html', inquilino=inquilino)

@admin_bp.route('/inquilinos/procesar', methods=['POST'])
def procesar_inquilino():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    datos = request.form.to_dict()
    try:
        if 'id_inquilino' in datos and datos['id_inquilino']:
            actualizar_inquilino(datos)
            flash('¡Inquilino actualizado exitosamente!', 'success')
        else:
            crear_inquilino(datos)
            flash('¡Inquilino creado exitosamente!', 'success')
    except Exception as e:
        flash(f'Error al procesar el inquilino: {e}', 'error')
    
    return redirect(url_for('admin.gestionar_inquilinos'))

@admin_bp.route('/inquilinos/eliminar/<int:id_inquilino>', methods=['POST'])
def eliminar_inquilino_route(id_inquilino):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    resultado = eliminar_inquilino(id_inquilino)
    flash(resultado['message'], resultado['status'])
    
    return redirect(url_for('admin.gestionar_inquilinos'))

# pago

@admin_bp.route('/pagos/registrar', methods=['POST'])
def registrar_pago_route():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    id_inquilino = request.form['id_inquilino']
    monto = request.form['monto_pagado']
    mes = request.form['mes_correspondiente']
    metodo = request.form['metodo_pago']

    resultado = registrar_pago(id_inquilino, monto, mes, metodo)
    flash(resultado['message'], resultado['status'])
    
    return redirect(url_for('admin.gestionar_inquilinos'))

@admin_bp.route('/inquilinos/<int:id_inquilino>/historial')
def historial_pagos_inquilino(id_inquilino):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    pagos = get_pagos_por_inquilino(id_inquilino)
    # También obtenemos los datos del inquilino para mostrar su nombre
    inquilino = get_inquilino_por_id(id_inquilino)
    
    if not inquilino:
        flash('Inquilino no encontrado.', 'error')
        return redirect(url_for('admin.gestionar_inquilinos'))
        
    return render_template('pages/admin/historial_pagos.html', pagos=pagos, inquilino=inquilino)

@admin_bp.route('/admins')
def gestionar_admins():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    admins = get_todos_los_admins()
    return render_template('pages/admin/gestionar_admins.html', admins=admins)

@admin_bp.route('/admins/nuevo')
def form_nuevo_admin():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    return render_template('pages/admin/form_admin.html', admin=None)

@admin_bp.route('/admins/editar/<int:id_admin>')
def form_editar_admin(id_admin):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    admin = get_admin_por_id(id_admin)
    return render_template('pages/admin/form_admin.html', admin=admin)

@admin_bp.route('/admins/procesar', methods=['POST'])
def procesar_admin():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    datos = request.form.to_dict()
    try:
        if 'id_administrador' in datos and datos['id_administrador']:
            # Lógica para no cambiar la contraseña si el campo está vacío al editar
            if not datos['password']:
                admin_actual = get_admin_por_id(datos['id_administrador'])
                datos['password'] = admin_actual['password']
            actualizar_admin(datos)
            flash('Administrador actualizado exitosamente.', 'success')
        else:
            crear_admin(datos)
            flash('Administrador creado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al procesar el administrador: {e}', 'error')
    
    return redirect(url_for('admin.gestionar_admins'))

@admin_bp.route('/admins/eliminar/<int:id_admin>', methods=['POST'])
def eliminar_admin_route(id_admin):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    # ¡¡CONTROL DE SEGURIDAD IMPORTANTE EN EL BACKEND!!
    # Compara el ID a eliminar con el ID del usuario en la sesión.
    if id_admin == session.get('user_id'):
        flash('Error: No puedes eliminar tu propia cuenta de administrador.', 'danger')
        return redirect(url_for('admin.gestionar_admins'))

    resultado = eliminar_admin(id_admin)
    flash(resultado['message'], resultado['status'])
    
    return redirect(url_for('admin.gestionar_admins'))