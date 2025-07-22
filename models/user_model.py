# Ya no necesitamos bcrypt, así que lo podemos quitar o comentar.
# import bcrypt 
from models.database import get_db_connection, release_db_connection

def verificar_credenciales(email, password_ingresada):
    """
    Verifica las credenciales comparando texto plano.
    ¡¡¡ADVERTENCIA: MÉTODO INSEGURO, SOLO PARA DESARROLLO!!!
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Buscar en la tabla de administradores
        # Seleccionamos la columna 'password' en lugar de 'password_hash'
        cursor.execute("SELECT id_administrador, nombres, password FROM administradores WHERE email = %s", (email,))
        admin = cursor.fetchone()

        if admin:
            id_admin, nombres_admin, password_guardada = admin
            # Comparamos directamente el texto de las contraseñas
            if password_ingresada == password_guardada:
                return {
                    'status': 'success', 
                    'role': 'admin', 
                    'data': {'id': id_admin, 'nombres': nombres_admin}
                }

        # 2. Si no es admin, buscar en la tabla de inquilinos
        cursor.execute("SELECT id_inquilino, nombres, estado, password FROM inquilinos WHERE email = %s", (email,))
        inquilino = cursor.fetchone()

        if inquilino:
            id_inquilino, nombres_inquilino, estado, password_guardada = inquilino
            
            if estado != 'activo':
                return {'status': 'error', 'message': 'La cuenta del inquilino no está activa.'}
            
            # Comparamos directamente el texto
            if password_ingresada == password_guardada:
                return {
                    'status': 'success', 
                    'role': 'inquilino', 
                    'data': {'id': id_inquilino, 'nombres': nombres_inquilino}
                }
        
        # 3. Si no se encontró en ninguna tabla o la contraseña no coincide
        return {'status': 'error', 'message': 'Email o contraseña incorrectos.'}

    except Exception as e:
        print(f"Error en la base de datos al verificar credenciales: {e}")
        return {'status': 'error', 'message': 'Ocurrió un error en el servidor.'}
    finally:
        if conn:
            release_db_connection(conn)