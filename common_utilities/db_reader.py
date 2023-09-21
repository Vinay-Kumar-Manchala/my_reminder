import psycopg2
from contextlib import contextmanager
from psycopg2.extras import RealDictCursor


class DbReader:
    def __init__(self):
        self.connection = psycopg2.connect(
            host="34.100.243.227",
            user="root",
            password="Secret@123",
            dbname="postgres",
            port="5432"
        )
        self.cursor_type = RealDictCursor

    @contextmanager
    def sql_connect(self):
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor

        finally:
            cursor.close()

    @contextmanager
    def dbconnect(self):
        try:
            yield self.connection
        finally:
            self.connection.close()