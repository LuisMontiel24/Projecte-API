from fastapi import FastAPI, HTTPException, File, UploadFile
import csv
import io
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from alumne_db import (
    read_alumnes,
    read_alumne_by_id,
    create_alumne,
    update_alumne,
    delete_alumne,
    read_alumnes_with_aula,
)
from client import db_client

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo Alumne
class Alumne(BaseModel):
    id: int
    nom: str
    cognom: str
    idAula: int

# Carga de Alumnos
@app.post("/alumne/loadAlumnes")
async def load_alumnes(file: UploadFile):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")

    try:
        content = await file.read()
        decoded_content = content.decode("utf-8").splitlines()
        reader = csv.reader(decoded_content)

        headers = next(reader)  
        expected_headers = ["id", "nom", "descAula", "edifici", "pis"]

        if headers != expected_headers:
            raise HTTPException(status_code=400, detail="El archivo CSV no tiene el formato correcto.")

        for row in reader:
            if len(row) != len(expected_headers):
                raise HTTPException(status_code=400, detail="El archivo CSV tiene un número incorrecto de columnas.")
            print(row) 

        return {"detail": "Archivo procesado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")

# Listar Alumnos
@app.get("/alumne/list", response_model=list[Alumne])
async def list_alumnes(orderby: str | None = None, contain: str | None = None, skip: int = 0, limit: int | None = None):
    alumnes = read_alumnes(orderby=orderby, contain=contain, skip=skip, limit=limit)

    if not alumnes:
        raise HTTPException(status_code=404, detail="No se encontraron alumnos")

    return [{"id": alumne[0], "nom": alumne[1], "cognom": alumne[2], "idAula": alumne[3]} for alumne in alumnes]

# Mostrar Alumne por ID
@app.get("/alumne/show/{id}")
async def show_alumne(id: int):
    alumne = read_alumne_by_id(id)
    if alumne is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    return {"alumne": {"id": alumne[0], "nom": alumne[1], "cognom": alumne[2], "idAula": alumne[3]}}

# Añadir Alumne
@app.post("/alumne/add")
async def add_alumne(alumne: Alumne):
    connection = db_client()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM aula WHERE id = %s", (alumne.idAula,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=400, detail="idAula no existe en la tabla Aula")
    
    success = create_alumne(alumne.nom, alumne.cognom, alumne.idAula)
    if not success:
        raise HTTPException(status_code=500, detail="Error al crear el alumno")

    connection.close()
    return {"message": "S’ha afegit correctament"}

# Actualizar Alumne
@app.put("/alumne/update/{id}")
async def update_alumne_endpoint(id: int, alumne: Alumne):
    connection = db_client()
    if connection is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM aula WHERE id = %s", (alumne.idAula,))
    if cursor.fetchone() is None:
        connection.close()
        raise HTTPException(status_code=400, detail="idAula no existe en la tabla Aula")
    
    try:
        cursor.execute(
            "UPDATE alumne SET nom = %s, cognom = %s, idAula = %s WHERE id = %s",
            (alumne.nom, alumne.cognom, alumne.idAula, id)
        )
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el alumno: {e}")

    finally:
        connection.close()

    return {"message": "S’ha modificat correctament"}

# Eliminar Alumne
@app.delete("/alumne/delete/{id}")
async def delete_alumne_endpoint(id: int):
    connection = db_client()
    if connection is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM alumne WHERE id = %s", (id,))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el alumno: {e}")

    finally:
        connection.close()

    return {"message": "S’ha esborrat correctament"}

# Listar Alumnos con Aula
@app.get("/alumne/listAll")
async def list_all_alumnes():
    alumnes = read_alumnes_with_aula()
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
