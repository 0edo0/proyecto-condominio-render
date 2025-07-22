from models.database import get_db_connection, release_db_connection
from psycopg2.extras import RealDictCursor
from datetime import datetime

def registrar_pago(id_inquilino, monto, mes_correspondiente, metodo_pago):
    """Inserta un nuevo pago en la base de datos."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO pagos (id_inquilino, fecha_pago, monto_pagado, mes_correspondiente, metodo_pago)
                 VALUES (%s, %s, %s, %s, %s)"""
        # Usamos CURRENT_DATE para registrar la fecha actual del pago
        cursor.execute(sql, (id_inquilino, datetime.now().date(), monto, mes_correspondiente, metodo_pago))
        conn.commit()
        return {'status': 'success', 'message': 'Pago registrado exitosamente.'}
    except Exception as e:
        conn.rollback()
        print(f"Error al registrar pago: {e}")
        return {'status': 'error', 'message': 'No se pudo registrar el pago.'}
    finally:
        if conn:
            release_db_connection(conn)

def get_pagos_por_inquilino(id_inquilino):
    """Obtiene todos los pagos realizados por un inquilino específico."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # Usamos la vista que ya tiene los datos del inquilino
        cursor.execute("SELECT * FROM vista_historial_pagos WHERE id_inquilino = %s ORDER BY fecha_pago DESC", (id_inquilino,))
        return cursor.fetchall()
    finally:
        if conn:
            release_db_connection(conn)