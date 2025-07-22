from models.database import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor

def get_todos_los_admins():
    """Obtiene todos los usuarios administradores de la base de datos."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM administradores ORDER BY apellidos, nombres")
        return cursor.fetchall()
    finally:
        if conn:
            release_db_connection(conn)

def get_admin_por_id(id_admin):
    """Obtiene un administrador específico por su ID."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM administradores WHERE id_administrador = %s", (id_admin,))
        return cursor.fetchone()
    finally:
        if conn:
            release_db_connection(conn)

def crear_admin(datos):
    """Inserta un nuevo administrador en la base de datos."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO administradores (nombres, apellidos, email, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (datos['nombres'], datos['apellidos'], datos['email'], datos['password']))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        if conn:
            release_db_connection(conn)

def actualizar_admin(datos):
    """Actualiza los datos de un administrador existente."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "UPDATE administradores SET nombres = %s, apellidos = %s, email = %s, password = %s WHERE id_administrador = %s"
        cursor.execute(sql, (datos['nombres'], datos['apellidos'], datos['email'], datos['password'], datos['id_administrador']))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        if conn:
            release_db_connection(conn)

def eliminar_admin(id_admin):
    """Elimina un administrador de la base de datos."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # La lógica para evitar la auto-eliminación se hará en el controlador,
        # que tiene acceso a la sesión del usuario.
        cursor.execute("DELETE FROM administradores WHERE id_administrador = %s", (id_admin,))
        conn.commit()
        return {'status': 'success', 'message': 'Administrador eliminado exitosamente.'}
    except Exception as e:
        conn.rollback()
        return {'status': 'error', 'message': f'Error al eliminar el administrador: {e}'}
    finally:
        if conn:
            release_db_connection(conn)