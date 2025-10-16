import psycopg2
from psycopg2 import OperationalError

DB_CONFIG = {
    "host": "ep-solitary-tree-ad6nnjhn-pooler.c-2.us-east-1.aws.neon.tech",
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_jZWg8HrBwo4L",
    "port": 5432,
    "sslmode": "require"
}

def test_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT version();")  # Consulta simple
        db_version = cur.fetchone()
        print("✅ Conexión exitosa a Neon.tech")
        print("📦 Versión del servidor PostgreSQL:", db_version[0])
        cur.close()
        conn.close()
    except OperationalError as e:
        print("❌ Error de conexión:", e)

if __name__ == "__main__":
    test_connection()