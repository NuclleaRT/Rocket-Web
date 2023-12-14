from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import pyodbc

#Ejecutar servidor local: uvicorn main:app --reload 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/usuario/")
async def insertarUsuario(nombre:str, apellido:str, rut:str, correo:str, telefono:str, direccion:str, estadoCivil:str):
    postUsuario(nombre, apellido, rut, correo, telefono, direccion, estadoCivil)
    return {"message": f"Usuario insertado"}

@app.get("/usuario/")
async def buscarUsuario():
    result = getUsuarios()
    if len(result) > 0:
        return {"message": f"Usuarios: {result}"}
    else:
        return {"message": "No hay usuarios registrados"}
    
#Funciones BD
def getUsuarios():
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=database.czvioqlcnkx5.us-east-2.rds.amazonaws.com;'
                              'Database=APIPROYECT;'
                              'UID=admin;'
                              'PWD=12345678;'
                              'PORT=1433;')

        cursor = conn.cursor()
        cursor.execute('execute BuscarUsuario')

        row = cursor.fetchall()

        cursor.close()
        conn.close()

        return row

    except Exception as e:
        print(e)

def postUsuario(nombre, apellido, rut, correo, telefono, direccion, estadoCivil):
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=database.czvioqlcnkx5.us-east-2.rds.amazonaws.com;'
                              'Database=APIPROYECT;'
                              'UID=admin;'
                              'PWD=12345678;'
                              'PORT=1433;')

        cursor = conn.cursor()
        cursor.execute('execute InsertaUsuario ?, ?, ?, ?, ?, ?, ?', nombre, apellido, rut, correo, telefono, direccion, estadoCivil)

        cursor.commit()
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)


        # Configuración de la conexión a SQL Server
server = "database.czvioqlcnkx5.us-east-2.rds.amazonaws.com"
database = "APIPROYECT"
username = "admin"
password = "12345678"

# Crear la cadena de conexión
conn_str = (
    f"Driver={{SQL Server}};"
    f"Server={server};"
    f"Database={database};"
    f"UID={username};"
    f"PWD={password};"
)

# Función para buscar un usuario por su RUT
def buscar_usuario_por_rut(rut):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Ejecutar la consulta para buscar al usuario por su RUT
        cursor.execute('execute BuscarUsuarioPorRut ?', rut)
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            return usuario
        else:
            # Si no se encontró el usuario, retornar None
            return None

    except Exception as e:
        print(f"Error de conexión: {str(e)}")
        return None

# Ruta para buscar un usuario por su RUT
@app.get("/buscar_usuario_por_rut/{rut}")
async def get_usuario_por_rut(rut: str):
    usuario = buscar_usuario_por_rut(rut)

    if usuario:
        # Formatear la respuesta como un diccionario JSON
        respuesta = {
           
            "cli_nombre": usuario[1],  
            "cli_apellido": usuario[2],  
            "cli_rut": usuario[3],  
            "cli_correo": usuario[4],
            "cli_telefono": usuario[5],  
            "cli_direccion": usuario[6],  
            "cli_estadocivil": usuario[7],
        }
        return respuesta
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")