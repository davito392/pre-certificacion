from base.models.cita_model import Cita
from base.models.usuario_model import usuario
from flask import render_template, redirect, request, session, Blueprint, flash

bp = Blueprint('citas', __name__, url_prefix='/citas')

@bp.route('/agregar', methods=['POST'])
def agregar_cita():
    if 'usuario_id' not in session:
        return redirect('/')
    if not Cita.validar_cita(request.form):
        return redirect('/citas')
    data = {
        'cita': request.form['cita'],
        'autor_id': session['usuario_id']
    }
    Cita.guardar_cita(data)
    flash('¡Cita agregada con éxito!', 'exito')
    return redirect('/citas')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def pagina_editar(id):
    if 'usuario_id' not in session:
        return redirect('/')
    cita = Cita.obtener_por_id(id)
    if not cita or cita.autor_id != session['usuario_id']:
        flash('No tienes permiso para editar esta cita.', 'error')
        return redirect('/citas')
    if request.method == 'POST':
        if not Cita.validar_cita(request.form):
            return render_template('edita_cita.html', cita=cita)
        data = {
            'id': id,
            'cita': request.form['cita']
        }
        Cita.actualizar_cita(data)
        flash('¡Cita actualizada!', 'exito')
        return redirect('/citas')
    return render_template('edita_cita.html', cita=cita)

@bp.route('/', methods=['GET'])
def listar_citas():
    if 'usuario_id' not in session:
        return redirect('/')
    citas = Cita.obtener_citas_usuarios(session['usuario_id'])
    return render_template('dashboard.html', citas=citas)

@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_cita(id):
    if 'usuario_id' not in session:
        return redirect('/')
    cita = Cita.obtener_por_id(id)
    if cita and cita.autor_id == session['usuario_id']:
        Cita.eliminar_cita(id)
        flash('¡Cita eliminada!', 'exito')
    else:
        flash('No tienes permiso para eliminar esta cita.', 'error')
    return redirect('/citas')
    
    
    