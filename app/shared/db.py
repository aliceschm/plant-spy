import psycopg

from app.shared.config import get_database_url


def get_connection():
    return psycopg.connect(get_database_url())