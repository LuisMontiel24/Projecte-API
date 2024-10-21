from client import db_client  # Para establecer la conexión a la base de datos
from mysql.connector import Error  # Para manejar errores de conexión y SQL

# Función para obtener todos los alumnos con soporte de parámetros de consulta (orderby, contain, skip, limit)
def read_alumnes(orderby: str | None = None, contain: str | None = None, skip: int = 0, limit: int | None = None):
    try:
        conn = db_client()  # Establecemos conexión a la base de datos
        cursor = conn.cursor()
        
        # Construcción de la consulta SQL básica
        query = "SELECT id, nom, cognom, idAula FROM alumne"
        params = []

        # Aplicar filtro de búsqueda si se proporciona 'contain'
        if contain:
            query += " WHERE nom LIKE %s"
            params.append(f"%{contain}%")

        # Aplicar ordenación si se proporciona 'orderby'
        if orderby:
            if orderby.lower() == 'asc':
                query += " ORDER BY nom ASC"
            elif orderby.lower() == 'desc':
                query += " ORDER BY nom DESC"

        # Aplicar paginación si se proporcionan 'skip' y 'limit'
        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params.append(limit)
            params.append(skip)

        cursor.execute(query, tuple(params))  # Ejecutamos la consulta con los parámetros
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
