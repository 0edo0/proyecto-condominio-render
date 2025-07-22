from models.database import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor

def get_todos_los_inquilinos():
    """Obtiene todos los inquilinos con información de su habitación si tienen una."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        sql = """
            SELECT i.*, h.numero_habitacion 
            FROM inquilinos i
            LEFT JOIN habitaciones h ON i.id_inquilino = h.id_inquilino
            ORDER BY i.apellidos, i.nombres;
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        if conn:
            release_db_connection(conn)

def get_inquilino_por_id(id_inquilino):
    """Obtiene los datos de un solo inquilino por su ID."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM inquilinos WHERE id_inquilino = %s", (id_inquilino,))
        return cursor.fetchone()
    finally:
        if conn:
            release_db_connection(conn)

def crear_inquilino(datos):
    """Inserta un nuevo inquilino en la base de datos."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO inquilinos (nombres, apellidos, dni, telefono, email, password, dia_pago_mensual, estado) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            datos['nombres'], datos['apellidos'], datos['dni'], 
            datos['telefono'], datos['email'], datos['password'], 
            datos['dia_pago_mensual'], datos['estado']
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        if conn:
            release_db_connection(conn)

def actualizar_inquilino(datos):
    """Actualiza los datos de un inquilino existente."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """UPDATE inquilinos SET 
                 nombres = %s, apellidos = %s, dni = %s, telefono = %s, 
                 email = %s, password = %s, dia_pago_mensual = %s, estado = %s 
                 WHERE id_inquilino = %s"""
        cursor.execute(sql, (
            datos['nombres'], datos['apellidos'], datos['dni'], 
            datos['telefono'], datos['email'], datos['password'], 
            datos['dia_pago_mensual'], datos['estado'], datos['id_inquilino']
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        if conn:
            release_db_connection(conn)

def eliminar_inquilino(id_inquilino):
    """Elimina un inquilino solo si no tiene una habitación asignada."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id_habitacion FROM habitaciones WHERE id_inquilino = %s", (id_inquilino,))
        habitacion_ocupada = cursor.fetchone()
        
        if habitacion_ocupada:
            return {'status': 'error', 'message': 'No se puede eliminar un inquilino que está ocupando una habitación.'}
            
        cursor.execute("DELETE FROM inquilinos WHERE id_inquilino = %s", (id_inquilino,))
        conn.commit()
        return {'status': 'success', 'message': 'Inquilino eliminado exitosamente.'}
    finally:
        if conn:
            release_db_connection(conn)

# ==========================================================
#      AQUÍ ESTÁ LA FUNCIÓN QUE FALTABA Y CAUSABA EL ERROR
# ==========================================================
def get_inquilinos_disponibles():
    """
    Obtiene una lista de inquilinos activos que no tienen una habitación asignada actualmente.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # Seleccionamos inquilinos cuyo ID no está en la columna id_inquilino de la tabla de habitaciones.
        sql = """
            SELECT id_inquilino, nombres, apellidos, dni FROM inquilinos 
            WHERE estado = 'activo' AND id_inquilino NOT IN (
                SELECT id_inquilino FROM habitaciones WHERE id_inquilino IS NOT NULL
            )
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        if conn:
            release_db_connection(conn)