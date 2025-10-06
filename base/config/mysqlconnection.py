# Importamos la librería pymysql para interactuar con MySQL
import pymysql.cursors

# Esta clase proporciona una instancia para conectarse a la base de datos MySQL


class MySQLConnection:
    # Método constructor que recibe el nombre de la base de datos como parámetro
    def __init__(self, db):
        # Configuración de la conexión, se pueden ajustar el usuario, la contraseña y otros parámetros según sea necesario
        self.connection = pymysql.connect(
            host='localhost',
            port=5307,  # Puerto estándar de MySQL
            user='root',       # Nombre de usuario de la base de datos
            password='root',  # Contraseña del usuario de la base de datos
            db=db,             # Nombre de la base de datos dinámico
            charset='utf8mb4',  # Codificación de caracteres
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    # Método para ejecutar consultas SQL en la base de datos
    # Recibe una consulta SQL (query) y opcionalmente datos (data) para consultas parametrizadas
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                # Si deseas depurar, imprime la consulta generada con mogrify
                if data:
                    print("Running Query:", cursor.mogrify(query, data))

                # Ejecutamos la consulta directamente
                cursor.execute(query, data)

                # Si la consulta es un INSERT, se devuelve el ID de la última fila insertada
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid

                # Si es una consulta SELECT, devolvemos el resultado como una lista de diccionarios
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result

                # Para consultas UPDATE o DELETE, confirmamos la transacción
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong", e)
                return False
            finally:
                # No cierres la conexión aquí, solo asegúrate de que el cursor se libere correctamente.
                pass

def connectToMySQL(db):
    return MySQLConnection(db)

