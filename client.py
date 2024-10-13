import mysql.connector  # Importar la biblioteca de conexión a MySQL
from mysql.connector import Error  # Importar para manejar errores

def db_client():
    """Establece una conexión a la base de datos MariaDB."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="Alumnat",
            user="root",
            password="123",
            port=3306,
            collation="utf8mb4_unicode_ci"
        )

        if connection.is_connected():
            print("Conexión exitosa.")
            return connection
        else:
            print("Conexión fallida.")

    except Error as e:
        print(f"Error al conectar: {e}")
        return None
