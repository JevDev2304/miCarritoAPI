import os


from dotenv import load_dotenv
import psycopg
from psycopg.errors import UniqueViolation

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

async def connect_db():
    try:
        # Establecer la conexión con la base de datos PostgreSQL
        conn = await psycopg.AsyncConnection.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        print("Conexión exitosa a la base de datos")
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para ejecutar una consulta de manera asíncrona y devolver un diccionario
async def execute_query(query: str, params: tuple = ()):
    connection = await connect_db()
    if connection:
        try:
            # Crear un cursor asíncrono
            async with connection.cursor() as cursor:
                # Ejecutar la consulta SQL con parámetros
                await cursor.execute(query, params)
                # Obtener las columnas (nombres de las columnas)
                columns = [desc[0] for desc in cursor.description]
                # Obtener los resultados de la consulta
                result = await cursor.fetchall()
                # Convertir los resultados a diccionarios
                dict_result = [dict(zip(columns, row)) for row in result]
                await connection.commit()
                return dict_result
        except UniqueViolation as e:
            raise e
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            raise e
        finally:
            # Cerrar la conexión después de la ejecución
            await connection.close()
