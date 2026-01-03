"""
Rutas generales de la aplicación.
Maneja las páginas generales como perfil y configuración.
"""
from flask import Blueprint, render_template

# Crear blueprint
general_bp = Blueprint('general', __name__)


@general_bp.route('/perfil')
def profile():
    """Página de perfil del usuario."""
    return render_template('page.html', title="Perfil", content="Esta es la página de perfil.")


@general_bp.route('/configuracion')
def settings():
    """Página de configuración."""
    return render_template('page.html', title="Configuración", content="Ajustes y preferencias aquí.")
