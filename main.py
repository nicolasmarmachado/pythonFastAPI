#API REST: Interfaz de programación de aplicaciones para compartir recursos

from typing import List, Optional
import uuid #generador de ID únicos
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#inicializamos una variable con todas las características de una API REST
app = FastAPI()

#Definimos el modelo
class Curso(BaseModel): 
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

#simulamos una base de datos
cursosdb = []

#CRUD: READ - CON MÉTODO GET. GET ALL = leeremos todos los cursos que haya en la bd

@app.get('/cursos/', response_model=List[Curso])
def obtenerCursos():
    return cursosdb

#CRUD: CREATE - METODO POST: agregaremos un nuevo recurso a la base de datos

@app.post('/cursos/', response_model=Curso)
def crearCurso(curso:Curso):
    curso.id = str(uuid.uuid4()) #usamos UUID para generar ID unicos e irrepetibles
    cursosdb.append(curso)
    return curso

#CRUD: READ - GET (individual): leeremos el curso que coincida con el ID que pidamos

@app.get('/cursos/{cursoId}', response_model=Curso)
def obtenerCurso(cursoId:str):
    curso = next((curso for curso in cursosdb if curso.id ==cursoId), None) #next devuelve la primera coincidencia, de lo contrario el FOR devuelve un array
    if curso is None: 
        raise HTTPException(status_code=404, detail='Curso no encontrado')
    return curso

#CRUD: UPDATE - PUT: modificaremos un recurso que coincida con el ID

@app.put('/cursos/{cursoId}', response_model=Curso)
def actualizarCurso(cursoId: str, cursoActualizado:Curso):
    curso = next((curso for curso in cursosdb if curso.id ==cursoId), None) #next devuelve la primera coincidencia, de lo contrario el FOR devuelve un array
    if curso is None: 
        raise HTTPException(status_code=404, detail='Curso no encontrado')
    cursoActualizado.id = cursoId
    index = cursosdb.index(curso) # buscamos el indice exacto donde está el curso en nuestra lista (db)
    cursosdb[index] = cursoActualizado
    return cursoActualizado

#CRUD: DELETE: Elimnamos un recurso que coincida con el ID

@app.delete('/cursos/{cursoId}', response_model=Curso)
def eliminarCurso(cursoId:str):
    curso = next((curso for curso in cursosdb if curso.id ==cursoId), None) #next devuelve la primera coincidencia, de lo contrario el FOR devuelve un array
    if curso is None: 
        raise HTTPException(status_code=404, detail='Curso no encontrado')
    return curso