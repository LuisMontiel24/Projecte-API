from client import db_client  # Para establecer la conexión a la base de datos
from mysql.connector import Error  # Para manejar errores de conexión y SQL


# Función para obtener todos los alumnos
def read_alumnes():
    try:
        conn = db_client()  # Establecemos conexión a la base de datos
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alumne")  # Ejecutamos la consulta para obtener todos los alumnos
        alumnes = cursor.fetchall()  # Recuperamos todos los registros
        conn.close()  # Cerramos la conexión
        return alumnes  # Devolvemos la lista de alumnos
    except Error as e:
        print(f"Error reading data: {e}")  # Imprimimos el error en caso de fallo
        return []
    
# Función para obtener un alumno por ID
def read_alumne_by_id(id):
    try:
        conn = db_client()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alumne WHERE id = %s", (id,))
        alumne = cursor.fetchone()
        conn.close()
        return alumne
    except Error as e:
        print(f"Error reading data: {e}")
        return None

# Función para agregar un nuevo alumno
def create_alumne(nom, cognom, idAula):
    try:
        conn = db_client()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alumne (nom, cognom, idAula) VALUES (%s, %s, %s)", (nom, cognom, idAula))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"Error inserting data: {e}")
        return False

# Función para actualizar un alumno
def update_alumne(id, nom, cognom, idAula):
    try:
        conn = db_client()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE alumne SET nom = %s, cognom = %s, idAula = %s WHERE id = %s",
            (nom, cognom, idAula, id)
        )
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating data: {e}")
        return False

# Función para eliminar un alumno
def delete_alumne(id):
    try:
        conn = db_client()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alumne WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"Error deleting data: {e}")
        return False

# Función para obtener la lista de alumnos con información del aula
def read_alumnes_with_aula():
    try:
        conn = db_client()
        cursor = conn.cursor()
        query = """
        SELECT a.id, a.nom, a.cognom, au.descAula, au.edifici, au.pis
        FROM alumne a
        JOIN aula au ON a.idAula = au.id
        """
        cursor.execute(query)
        alumnes = cursor.fetchall()
        conn.close()
        return alumnes
    except Error as e:
        print(f"Error reading data: {e}")
        return []