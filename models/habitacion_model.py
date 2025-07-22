from models.database import get_db_connection, release_db_connection
# ¡CAMBIO IMPORTANTE! Importamos el cursor especial de psycopg2
from psycopg2.extras import RealDictCursor

def get_todas_las_habitaciones():
    """Obtiene todas las habitaciones con detalles del inquilino si está ocupada."""
    conn = None
    try:
        conn = get_db_connection()
        # ¡CORRECCIÓN! Usamos el 'cursor_factory' para que devuelva diccionarios.
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM vista_habitaciones_completa ORDER BY numero_habitacion")
        habitaciones = cursor.fetchall()
        return habitaciones
    finally:
        if conn:
            release_db_connection(conn)

def get_habitacion_por_id(id_habitacion):
    """Obtiene los datos de una sola habitación por su ID."""
    conn = None
    try:
        conn = get_db_connection()
        # ¡CORRECCIÓN! Aplicamos el mismo cambio aquí.
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM habitaciones WHERE id_habitacion = %s", (id_habitacion,))
        return cursor.fetchone()
    finally:
        if conn:
            release_db_connection(conn)

def crear_habitacion(datos):
    """Inserta una nueva habitación en la base de datos."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor() # Aquí no necesitamos diccionarios, así que se queda normal.
        sql = """INSERT INTO habitaciones (id_condominio, numero_habitacion, descripcion, monto_alquiler, estado) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (1, datos['numero_habitacion'], datos['descripcion'], datos['monto_alquiler'], datos['estado']))
        conn.commit()
    finally:
        if conn:
            release_db_connection(conn)

def actualizar_habitacion(datos):
    """Actualiza los datos de una habitación existente."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor() # Aquí tampoco es necesario.
        sql = """UPDATE habitaciones SET 
                 numero_habitacion = %s, 
                 descripcion = %s, 
                 monto_alquiler = %s, 
                 estado = %s 
                 WHERE id_habitacion = %s"""
        cursor.execute(sql, (datos['numero_habitacion'], datos['descripcion'], datos['monto_alquiler'], datos['estado'], datos['id_habitacion']))
        conn.commit()
    finally:
        if conn:
            release_db_connection(conn)

def eliminar_habitacion(id_habitacion):
    """Elimina una habitación si no está ocupada."""
    conn = None
    try:
        conn = get_db_connection()
        # ¡CORRECCIÓN! Aquí sí necesitamos el diccionario para leer el 'id_inquilino'.
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id_inquilino FROM habitaciones WHERE id_habitacion = %s", (id_habitacion,))
        habitacion = cursor.fetchone()
        if habitacion and habitacion['id_inquilino'] is not None:
            return {'status': 'error', 'message': 'No se puede eliminar una habitación que está ocupada.'}

        cursor.execute("DELETE FROM habitaciones WHERE id_habitacion = %s", (id_habitacion,))
        conn.commit()
        return {'status': 'success', 'message': 'Habitación eliminada exitosamente.'}
    finally:
        if conn:
            release_db_connection(conn)
def asignar_inquilino_a_habitacion(id_habitacion, id_inquilino):
    """Asigna un inquilino a una habitación y la marca como 'ocupada'."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # El trigger que creamos en la BD se encargará de cambiar el estado a 'ocupada' automáticamente.
        sql = "UPDATE habitaciones SET id_inquilino = %s WHERE id_habitacion = %s"
        cursor.execute(sql, (id_inquilino, id_habitacion))
        conn.commit()
        return {'status': 'success', 'message': 'Inquilino asignado exitosamente.'}
    except Exception as e:
        print(e)
        return {'status': 'error', 'message': 'Error al asignar el inquilino.'}
    finally:
        if conn:
            release_db_connection(conn)

def finalizar_alquiler(id_habitacion):
    """Libera una habitación y marca al inquilino anterior como 'inactivo'."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor) # Usamos RealDictCursor para leer el id_inquilino
        
        # Obtenemos el ID del inquilino que se va
        cursor.execute("SELECT id_inquilino FROM habitaciones WHERE id_habitacion = %s", (id_habitacion,))
        habitacion = cursor.fetchone()
        
        if not habitacion or habitacion['id_inquilino'] is None:
            return {'status': 'error', 'message': 'Esta habitación no tiene un alquiler activo.'}
        
        id_inquilino_anterior = habitacion['id_inquilino']

        # Usamos la función de la BD que creamos, es más seguro y atómico.
        cursor.execute("SELECT finalizar_ocupacion(%s)", (id_habitacion,))
        conn.commit()
        
        return {'status': 'success', 'message': 'Alquiler finalizado correctamente.'}
    except Exception as e:
        print(e)
        return {'status': 'error', 'message': 'Error al finalizar el alquiler.'}
    finally:
        if conn:
            release_db_connection(conn)
            
def get_habitacion_por_inquilino_id(id_inquilino):
    """Obtiene los detalles de la habitación que ocupa un inquilino."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM habitaciones WHERE id_inquilino = %s", (id_inquilino,))
        return cursor.fetchone()
    finally:
        if conn:
            release_db_connection(conn)