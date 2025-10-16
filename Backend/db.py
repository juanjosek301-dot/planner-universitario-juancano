import psycopg2
import SecretConfig  

def get_connection():
    return psycopg2.connect(
        database=SecretConfig.PGDATABASE,
        user=SecretConfig.PGUSER,
        password=SecretConfig.PGPASSWORD,
        host=SecretConfig.PGHOST,
        port=SecretConfig.PGPORT
    )