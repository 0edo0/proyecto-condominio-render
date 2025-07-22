# models/database.py
import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

db_pool = None
# Render proveerá esta variable de entorno automáticamente
database_url = os.environ.get('DATABASE_URL')

try:
    # Si existe DATABASE_URL (estamos en Render/producción)
    if database_url:
        print("✓ Conectando a la base de datos de producción en Render...")
        db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, dsn=database_url)
    # Si no, usamos las variables locales de .env (estamos en desarrollo)
    else:
        print("✓ Conectando a la base de datos local...")
        db_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1, maxconn=10,
            user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME')
        )
except Exception as e:
    print(f"FATAL: No se pudo conectar a la base de datos. Error: {e}")
    db_pool = None

def get_db_connection():
    if db_pool: return db_pool.getconn()
    raise Exception("El pool de la base de datos no está disponible.")

def release_db_connection(conn):
    if db_pool: db_pool.putconn(conn)

print("✓ Módulo de base de datos cargado.")