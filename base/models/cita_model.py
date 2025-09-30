from base.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Cita:
    """
    Modelo para la gestión de citas en la base de datos.
    """
    db = "proyecto_crud"

    def __init__(self, data):
        self.id = data['id']
        self.cita = data['citas']  # Asegúrate que el campo en la BD se llama 'citas'
        self.autor_id = data['autor_id']
        self.usuario_id = data['usuario_id']
        self.creado_en = data['creado_en']
        self.actualizado_en = data['actualizado_en']

    @classmethod
    def obtener_citas_usuarios(cls, usuario_id):
        query = "SELECT * FROM citas WHERE autor_id = %(usuario_id)s"
        data = {'usuario_id': usuario_id}
        resultado = connectToMySQL(cls.db).query_db(query, data)
        citas = []
        if resultado:
            for row in resultado:
                citas.append(cls(row))
        return citas

    @classmethod
    def guardar_cita(cls, data):
        query = "INSERT INTO citas (citas, autor_id) VALUES (%(citas)s, %(autor_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def obtener_por_id(cls, cita_id):
        query = "SELECT * FROM citas WHERE id = %(id)s;"
        data = {'id': cita_id}
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])

    @classmethod
    def obtener_todas(cls):
        query = "SELECT * FROM citas;"
        resultado = connectToMySQL(cls.db).query_db(query)
        citas = []
        if resultado:
            for row in resultado:
                citas.append(cls(row))
        return citas

    @classmethod
    def actualizar_cita(cls, data):
        query = "UPDATE citas SET citas = %(citas)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def eliminar_cita(cls, cita_id):
        query = "DELETE FROM citas WHERE id = %(id)s;"
        data = {'id': cita_id}
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validar_cita(cita):
        is_valid = True
        if len(cita['cita']) < 5:
            flash("La cita debe tener al menos 5 caracteres.", 'alerta')
            is_valid = False
        # Aquí puedes agregar más validaciones si lo necesitas
        return is_valid

    def to_dict(self):
        """
        Convierte la instancia en un diccionario.
        """
        return {
            'id': self.id,
            'cita': self.cita,
            'autor_id': self.autor_id,
            'usuario_id': self.usuario_id,
            'creado_en': self.creado_en,
            'actualizado_en': self.actualizado_en
        }
        
        