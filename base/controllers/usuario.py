from flask import render_template, redirect, request, session, flash
from base.models.usuario_model import usuario
from bcrypt import hashpw, gensalt

from flask import Blueprint
bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@bp.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    if not usuario.validar_registro(request.form):
        return redirect('/')
    password_hash = hashpw(request.form['password'].encode('utf-8'), gensalt())
    data = {
        **request.form,
        'password': password_hash.decode('utf-8')
    }
    usuario_id = usuario.guardar_usuario(data)
    session['usuario_id'] = usuario_id
    flash("¡Su cuenta ha sido registrada con éxito!", 'exito')
    return redirect('/dashboard')

@bp.route('/procesar_login', methods=['POST'])
def procesar_login():
    if not usuario.validar_login(request.form):
        return redirect('/')
    usuario_db = usuario.obtener_por_email(request.form)
    session['usuario_id'] = usuario_db.id
    flash(f"¡Bienvenido de nuevo, {usuario_db.nombre}!")
    return redirect('/dashboard')
    