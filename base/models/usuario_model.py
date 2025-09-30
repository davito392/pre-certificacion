from base.config.mysqlconnection import connectToMySQL
import re 
from flask import flash, session
from bcrypt import hashpw, gensalt, checkpw


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]+$')

class usuario:
    """
    Clase que representa a un usuario y sus operaciones en la base de datos 
    """
    bd = "proyecto_crud"
    
    def __init__(self, data):
        """
        Constructor: inicializa los atributos del usuario
        """
        self.id= data['id']
        self.nombre = data['nombre'].capitalize()
        self.apellido = data ['apellido'].capitalize()
        self.email = data['email']
        self.password = data['password']
        self.creado_en = data['creado_en']
        self.creado_en = data['creado_en']
        self.actualizado_en = data['actualizado_en']
        

    @classmethod
    def guardar_usuario(cls, data):
        """
        Guardar un nuevo usuario en la base de datos y devolver su id
        """
        data['nombre'] = data['nombre'].capitalize()
        data['apellido'] = data['apellido'].capitalize()
        query = "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.bd).query_db(query, data)
        

    @classmethod
    def obtener_por_email(cls, data):
        """
        Buscar Usuario por su email
        """
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(cls.bd).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])

    @classmethod
    def obtener_por_id(cls, usuario_id):
        """
        Buscar un usuario por su iID 
        """
        query = "SELECT * FROM usuarios WHERE id = %(id)s"
        data = {'id': usuario_id}
        resultado = connectToMySQL(cls.bd).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])

    @classmethod
    def validar_registro(cls, usuario):
        """
        Valida los datos del formulario de registro.
        devuelve True si todo es valido, False si hay errores (y los muestra con flash).
        """
        is_valid = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(cls.bd).query_db(query, usuario)
        if resultado:
            flash("el email ya esta registrado.", 'registro')
            is_valid = False
        if not EMAIL_REGEX.match(usuario['email']):
            flash("formato de email es invalido", 'registro')
            is_valid = False
        if len(usuario['nombre']) < 3:
            flash("El nombre debe tener al menos 3 caracteres.", 'registro')
            is_valid = False
        if len(usuario['apellido']) < 3:
            flash("El apellido debe tener al menos 3 caracteres.", 'registro')
            is_valid = False
        if len(usuario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", 'registro')
            is_valid = False
        if usuario['password'] != usuario.get('confirm_password', ''):
            flash("las contraseñas no coinciden.", 'registro')
            is_valid = False
        return is_valid 
            
    @staticmethod
    def validar_login(usuario):
        is_valid = True
        user_in_db = usuario.obtener_por_email(usuario)
        if not user_in_db:
            flash("Email no registrado.", 'login')
            is_valid = False 
        else:
            if not checkpw(usuario['password'].encode('utf-8'), user_in_db.password.encode('utf-8')):
                flash("contraseña incorrecta.", 'login')
                is_valid = False
        return is_valid
    
    
           
        