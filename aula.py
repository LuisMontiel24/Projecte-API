from client import db_client  # Para establecer la conexión a la base de datos
from mysql.connector import Error  # Para manejar errores de conexión y SQL

# Esquema de Aula
def aula_schema(aula) -> dict:
    """Convierte un registro de aula en un diccionario."""
    return {
        "IdAula": aula[0],
        "DesAula": aula[1],
        "Edifici": aula[2],
        "Pis": aula[3],
    }

def aula_schema_list(aules) -> list:
    """Convierte una lista de aulas en una lista de diccionarios."""
    return [aula_schema(aula) for aula in aules]

def read_aules():
    """Obtiene todas las aulas de la base de datos."""
    try:
        connection = db_client()
        if connection is None:
            print("No se pudo establecer conexión.")
            return []

        cursor = connection.cursor()
        query = "SELECT * FROM aula"
        cursor.execute(query)
        aules = cursor.fetchall()

        return aula_schema_list(aules)

    except Error as e:
        print(f"Error al leer datos de aulas: {e}")
        return []
    
    finally:
        if connection and connection.is_connected():
            connection.close()