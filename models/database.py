import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

# --- Configuración del Pool de Conexiones ---
# Usar un pool de conexiones es mucho más eficiente que abrir y cerrar
# conexiones para cada consulta.
db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME')
)

def get_db_connection():
    """Obtiene una conexión del pool."""
    return db_pool.getconn()

def release_db_connection(conn):
    """Devuelve una conexión al pool."""
    db_pool.putconn(conn)

def close_all_connections():
    """Cierra todas las conexiones del pool al finalizar la aplicación."""
    db_pool.closeall()

print("✓ Módulo de base de datos cargado correctamente.")