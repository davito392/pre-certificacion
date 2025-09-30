from flask import Flask, render_template
from datetime import datetime
from base.controllers.citas import bp as citas_bp
## from base.controllers.planes import bp as planes_bp

# Filtro de Jinja2 para formatear fechas
def format_date(value, format='%Y-%m-%d'):
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d')
    return value.strftime(format)

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG=True,
    )
    app.register_blueprint(citas_bp)
    # app.register_blueprint(planes_bp)
    app.add_template_filter(format_date, 'format_date')


    @app.route('/')
    def index():
        return render_template('auth.html')

    @app.route('/dashboard')
    def dashboard():
        from base.models.cita_model import Cita
        from flask import session, redirect
        if 'usuario_id' not in session:
            return redirect('/')
        citas = Cita.obtener_citas_usuarios(session['usuario_id'])
        return render_template('dashboard.html', citas=citas)

    return app


