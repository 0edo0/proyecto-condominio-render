from models.database import get_db_connection, release_db_connection
from datetime import datetime
# ==========================================================
#      ¡CORRECCIÓN! AÑADIMOS LA IMPORTACIÓN QUE FALTABA
# ==========================================================
from psycopg2.extras import RealDictCursor

def get_eventos_admin():
    """
    Obtiene los eventos de pago para el calendario del administrador.
    Usa la vista de deudas para determinar el estado.
    """
    eventos = []
    conn = None
    try:
        conn = get_db_connection()
        # Aquí ya estaba correcto porque lo habíamos arreglado antes
        cursor = conn.cursor(cursor_factory=RealDictCursor) 

        query = "SELECT nombres, apellidos, dia_pago_mensual, deuda_restante FROM vista_reporte_deudas_actual"
        cursor.execute(query)
        
        registros = cursor.fetchall()
        
        hoy = datetime.now()
        año_actual = hoy.year
        mes_actual = hoy.month

        for reg in registros:
            dia_pago = reg['dia_pago_mensual']
            fecha_evento = f"{año_actual}-{mes_actual:02d}-{dia_pago:02d}"
            
            clase_css = 'fc-event-pagado' if reg['deuda_restante'] <= 0 else 'fc-event-pendiente'
            
            evento = {
                "title": f"Pago: {reg['nombres']} {reg['apellidos']}",
                "start": fecha_evento,
                "className": clase_css
            }
            eventos.append(evento)

        return eventos

    except Exception as e:
        print(f"Error al obtener eventos del calendario: {e}")
        return []
    finally:
        if conn:
            release_db_connection(conn)


def get_eventos_inquilino(id_inquilino):
    """Obtiene los eventos de pago para el calendario de un inquilino específico."""
    conn = None
    try:
        conn = get_db_connection()
        # Aquí estaba el error, pero ahora la importación lo soluciona.
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT dia_pago_mensual FROM inquilinos WHERE id_inquilino = %s", (id_inquilino,))
        inquilino = cursor.fetchone()

        if not inquilino:
            return []
        
        hoy = datetime.now()
        año_actual = hoy.year
        mes_actual = hoy.month
        dia_pago = inquilino['dia_pago_mensual']
        
        eventos = []
        for i in range(12):
            mes_evento = (mes_actual - 1 + i) % 12 + 1
            año_evento = año_actual + (mes_actual - 1 + i) // 12
            fecha_evento = f"{año_evento}-{mes_evento:02d}-{dia_pago:02d}"
            eventos.append({
                "title": "Mi Día de Pago",
                "start": fecha_evento,
                "backgroundColor": '#0d6efd',
                "borderColor": '#0d6efd'
            })
        return eventos
    except Exception as e:
        print(f"Error al obtener eventos del inquilino: {e}")
        return []
    finally:
        if conn:
            release_db_connection(conn)