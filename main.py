from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from alumne_db import (
    read_alumnes,
    read_alumne_by_id,
    create_alumne,
    update_alumne,
    delete_alumne,
    read_alumnes_with_aula
)
# Importa las funciones necesarias desde alumne_db.py
from client import db_client

app = FastAPI()

# 2. Definición del Modelo Alumne
class Alumne(BaseModel):
    id: int
    nom: str
    cognom: str
    idAula: int

# 3. Ruta: Listar Todos los Alumnos
@app.get("/alumne/list", response_model=list[Alumne])
async def list_alumnes():
    alumnes = read_alumnes()  # Obtiene los alumnos
    if not alumnes:
        raise HTTPException(status_code=404, detail="No se encontraron alumnos")
    
    # Devuelve la lista de alumnos en el formato del modelo Alumne
    return [{"id": alumne[0], "nom": alumne[1], "cognom": alumne[2], "idAula": alumne[3]} for alumne in alumnes]

# 4. Ruta: Mostrar un Alumno Específico por ID
@app.get("/alumne/show/{id}")
async def show_alumne(id: int):
    alumne = read_alumne_by_id(id)  # Obtiene el alumno por ID
    if alumne is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    # Retorna los detalles del alumno
    return {"alumne": {"id": alumne[0], "nom": alumne[1], "cognom": alumne[2], "idAula": alumne[3]}}

# 5. Ruta: Añadir un Nuevo Alumno
@app.post("/alumne/add")
async def add_alumne(alumne: Alumne):
    connection = db_client()  # Conecta a la base de datos
    cursor = connection.cursor()
    
    # Verifica si el idAula existe en la tabla Aula
    cursor.execute("SELECT * FROM aula WHERE id = %s", (alumne.idAula,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=400, detail="idAula no existe en la tabla Aula")
    
    # Intenta crear el nuevo alumno
    success = create_alumne(alumne.nom, alumne.cognom, alumne.idAula)
    if not success:
        raise HTTPException(status_code=500, detail="Error al crear el alumno")

    connection.close()  # Cierra la conexión
    return {"message": "S’ha afegit correctament"}

# 6. Ruta: Actualizar un Alumno Existente
@app.put("/alumne/update/{id}")
async def update_alumne_endpoint(id: int, alumne: Alumne):
    connection = db_client()  # Conecta a la base de datos
    if connection is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    cursor = connection.cursor()

    # Verifica si el ID del aula existe en la tabla Aula
    cursor.execute("SELECT * FROM aula WHERE id = %s", (alumne.idAula,))
    if cursor.fetchone() is None:
        connection.close()  # Cierra la conexión antes de retornar
        raise HTTPException(status_code=400, detail="idAula no existe en la tabla Aula")
    
    # Intenta actualizar la información del alumno
    try:
        cursor.execute(
            "UPDATE alumne SET nom = %s, cognom = %s, idAula = %s WHERE id = %s",
            (alumne.nom, alumne.cognom, alumne.idAula, id)
        )  # Actualiza el alumno
        connection.commit()  # Confirma los cambios

        if cursor.rowcount == 0:  # Verifica si se actualizó algún registro
            raise HTTPException(status_code=404, detail="Alumno no encontrado")

    except Exception as e:
        connection.rollback()  # Revierte cambios si ocurre un error
        raise HTTPException(status_code=500, detail=f"Error al actualizar el alumno: {e}")

    finally:
        connection.close()  # Cierra la conexión

    return {"message": "S’ha modificat correctament"}

# 7. Ruta: Eliminar un Alumno
# Elimina un alumno de la base de datos
@app.delete("/alumne/delete/{id}")
async def delete_alumne_endpoint(id: int):
    connection = db_client()  # Conecta a la base de datos
    if connection is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    cursor = connection.cursor()

    # Intenta eliminar el alumno
    try:
        cursor.execute("DELETE FROM alumne WHERE id = %s", (id,))
        connection.commit()  # Confirma los cambios

        if cursor.rowcount == 0:  # Verifica si se eliminó algún registro
            raise HTTPException(status_code=404, detail="Alumno no encontrado")

    except Exception as e:
        connection.rollback()  # Revierte cambios si ocurre un error
        raise HTTPException(status_code=500, detail=f"Error al eliminar el alumno: {e}")

    finally:
        connection.close()  # Cierra la conexión

    return {"message": "S’ha esborrat correctament"}
    

# 8. Ruta: Listar Todos los Alumnos con Información del Aula
@app.get("/alumne/listAll")
async def list_all_alumnes():
    alumnes = read_alumnes_with_aula()  # Obtiene los alumnos junto con sus aulas
    return {
        "alumnes": [
            {
                "id": alumne[0],
                "nom": alumne[1],
                "cognom": alumne[2],
                "descAula": alumne[3],
                "edifici": alumne[4],
                "pis": alumne[5]
            }
            for alumne in alumnes
        ]
    }
