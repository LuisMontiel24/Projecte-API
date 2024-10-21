from pydantic import BaseModel

class AlumneSchema(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: str
    Grup: str
    DescAula: str
    
def alumne_schema(fetchalumne) -> dict:
    return{
        "NomAlumne":  fetchalumne[1],
        "Cicle":  fetchalumne[2],
        "Curs":   fetchalumne[3],
        "Grup": fetchalumne [4],
        "DescAula"  : fetchalumne[5],    
    }
def alumnes_schema(alumnes) -> list:
    return [alumne_schema(alumne) for alumne in alumnes]