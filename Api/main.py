from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyodbc

#Ejecutar servidor local: uvicorn main:app --reload 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#---------------------------------------------------------------------------------------------------------------------------------------------
class UsuarioIn(BaseModel):
    rut: str
    nombre: str
    apellido: str
    correo: str
    telefono: int
    clave: str

@app.put("/usuario/")
async def IngresarUsuario(usuario: UsuarioIn):
    postUsuario(usuario.rut, usuario.nombre, usuario.apellido, usuario.correo, usuario.telefono, usuario.clave)
    return {"mensaje": "Usuario Ingresado correctamente"}


def postUsuario(rut, nombre, apellido, correo, telefono, clave ):
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=rocket-web.cp3jerhhedbh.us-east-2.rds.amazonaws.com;'
                              'Database=ROCKET_3D;'
                              'UID=admin;'
                              'PWD=admin1234;'
                              'PORT=1433;')

        cursor = conn.cursor()
        cursor.execute('execute IngresarUsuario ?, ?, ?, ?, ?, ?', rut, nombre, apellido, correo, telefono, clave)

        cursor.commit()
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        
#---------------------------------------------------------------------------------------------------------------------------------------------        
class LoginRequest(BaseModel):
    correo: str
    clave: str

@app.post("/login/")
async def iniciar_sesion(login_request: LoginRequest):
    # Lógica para verificar el inicio de sesión
    # Aquí deberías verificar en tu base de datos si el correo y la clave son válidos
    # Si son válidos, puedes generar un token de sesión y devolverlo en la respuesta

    # Ejemplo simple de verificación (esto debe adaptarse a tu lógica real)
    if verificar_credenciales(login_request.correo, login_request.clave):
        # Aquí, deberías generar y devolver un token de sesión (usando JWT, por ejemplo)
        # También podrías manejar otras lógicas de sesión o cookies, según tus necesidades
        return {"mensaje": "Inicio de sesión exitoso"}
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

def verificar_credenciales(correo, clave):
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=rocket-web.cp3jerhhedbh.us-east-2.rds.amazonaws.com;'
                              'Database=ROCKET_3D;'
                              'UID=admin;'
                              'PWD=admin1234;'
                              'PORT=1433;')

        cursor = conn.cursor()
        cursor.execute('EXEC LoginUsuario ?, ?', correo, clave)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result is not None  # Devuelve True si se encontró un usuario con las credenciales proporcionadas
    except Exception as e:
        print(e)
        return False


#---------------------------------------------------------------------------------------------------------------------------------------------

from typing import List

class Producto(BaseModel):
    id: int
    nombre: str
    precio: int
    descripcion: str

@app.get("/productos-recomendados/", response_model=List[Producto])
async def obtener_productos_recomendados():
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=rocket-web.cp3jerhhedbh.us-east-2.rds.amazonaws.com;'
                              'Database=ROCKET_3D;'
                              'UID=admin;'
                              'PWD=admin1234;'
                              'PORT=1433;')

        cursor = conn.cursor()
        cursor.execute('EXEC ObtenerUltimosProductos')
        results = cursor.fetchall()

        productos = []
        for row in results:
            producto = {
                "id": row.PRO_ID,
                "nombre": row.PRO_NOMBRE,
                "precio": row.PRO_PRECIO,
                "descripcion": row.PRO_DESCRIPCION
            }
            productos.append(producto)

        cursor.close()
        conn.close()

        return productos
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error al obtener productos recomendados")



#---------------------------------------------------------------------------------------------------------------------------------------------

class Product(BaseModel):
    id: int
    nombre: str
    precio: int
    descripcion: str

@app.get("/products/catalog")
async def obtener_catalogo():
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=rocket-web.cp3jerhhedbh.us-east-2.rds.amazonaws.com;'
                              'Database=ROCKET_3D;'
                              'UID=admin;'
                              'PWD=admin1234;'
                              'PORT=1433;')

        cursor = conn.cursor()
        cursor.execute('EXEC ObtenerCatalogo')
        products = []
        for row in cursor.fetchall():
            product = Product(id=row.PRO_ID, nombre=row.PRO_NOMBRE, precio=row.PRO_PRECIO, descripcion=row.PRO_DESCRIPCION)
            products.append(product)

        cursor.close()
        conn.close()

        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#---------------------------------------------------------------------------------------------------------------------------------------------


@app.get("/products/search")
async def search_products(query: str):
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=rocket-web.cp3jerhhedbh.us-east-2.rds.amazonaws.com;'
                              'Database=ROCKET_3D;'
                              'UID=admin;'
                              'PWD=admin1234;'
                              'PORT=1433;')

        cursor = conn.cursor()
        cursor.execute('EXEC FiltrarProducto @filtroNombre = ?', query)
        products = []
        for row in cursor.fetchall():
            product = Product(id=row.PRO_ID, nombre=row.PRO_NOMBRE, precio=row.PRO_PRECIO, descripcion=row.PRO_DESCRIPCION)
            products.append(product)

        cursor.close()
        conn.close()

        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#---------------------------------------------------------------------------------------------------------------------------------------------


# En tu API, agrega un nuevo endpoint para obtener detalles de un producto por id
@app.get("/products/details/{product_id}")
async def obtener_detalles_producto(product_id: int):
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=rocket-web.cp3jerhhedbh.us-east-2.rds.amazonaws.com;'
                              'Database=ROCKET_3D;'
                              'UID=admin;'
                              'PWD=admin1234;'
                              'PORT=1433;')

        cursor = conn.cursor()
        cursor.execute('EXEC ObtenerDetallesProducto @ProductId = ?', product_id)
        row = cursor.fetchone()

        if row:
            # Supongamos que ObtenerDetallesProducto devuelve detalles del producto
            detalles_producto = {
                'id': row.PRO_ID,
                'nombre': row.PRO_NOMBRE,
                'precio': row.PRO_PRECIO,
                'descripcion': row.PRO_DESCRIPCION,
                'vista3D': row.PRO_VISTA_3D,
                # Otros campos que puedan ser relevantes
            }

            return detalles_producto
        else:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
        
        
        
#---------------------------------------------------------------------------------------------------------------------------------------------
from datetime import datetime
from datetime import date 
from fastapi import Depends, HTTPException
from fastapi import FastAPI, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
import pyodbc

from fastapi import HTTPException

class DetalleCompra(BaseModel):
    ped_id: int
    pro_id: int
    nombre_producto: str
    cantidad: int
    precio_unitario: float

class CompraRequest(BaseModel):
    detalles: List[DetalleCompra]

@app.post("/realizar_compra/")
async def realizar_compra(compra_request: CompraRequest):
    try:
        conn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=rocket-web.cp3jerhhedbh.us-east-2.rds.amazonaws.com;'
            'Database=ROCKET_3D;'
            'UID=admin;'
            'PWD=admin1234;'
            'PORT=1433;')

        cursor = conn.cursor()

        for detalle in compra_request.detalles:
            print(f"Insertando detalle: {detalle}")

            cursor.execute(
                'EXEC InsertarDetalleCompra ?, ?, ?, ?, ?',
                detalle.ped_id,
                detalle.pro_id,
                detalle.nombre_producto,
                detalle.cantidad,
                detalle.precio_unitario
            )

        conn.commit()
        cursor.close()
        conn.close()

        return {"mensaje": "Compra realizada exitosamente"}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error al realizar la compra")





#---------------------------------------------------------------------------------------------------------------------------------------------

