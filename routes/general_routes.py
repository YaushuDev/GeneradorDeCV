"""
Rutas generales de la aplicación.
Maneja las páginas generales como perfil y configuración.
"""
from flask import Blueprint, render_template, request, jsonify
from services.data_service import DataService
from config.settings import Config

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


@general_bp.route('/prompt-ia')
def prompt_ia():
    """Página de Prompt IA."""
    return render_template('prompt_ia.html', title="Prompt IA")


@general_bp.route('/get_prompt', methods=['GET'])
def get_prompt():
    """Recupera el prompt guardado."""
    service = DataService(Config.PROMPTS_DATA_FILE)
    data = service.load_raw()
    return jsonify(data)


@general_bp.route('/save_prompt', methods=['POST'])
def save_prompt():
    """Guarda el prompt del usuario."""
    data = request.json
    service = DataService(Config.PROMPTS_DATA_FILE)
    if service.save_raw(data):
        return jsonify({"success": True})
    return jsonify({"success": False}), 500


@general_bp.route('/registro-empleo')
def registro_empleo():
    """Página de Registro de Empleos."""
    return render_template('registro_empleo.html', title="Registro Empleo")


@general_bp.route('/get_empleos', methods=['GET'])
def get_empleos():
    """Recupera los empleos guardados."""
    service = DataService(Config.EMPLEOS_DATA_FILE)
    data = service.load_raw()
    return jsonify(data)


@general_bp.route('/save_empleos', methods=['POST'])
def save_empleos():
    """Guarda los empleos del usuario."""
    data = request.json
    service = DataService(Config.EMPLEOS_DATA_FILE)
    if service.save_raw(data):
        return jsonify({"success": True})
    return jsonify({"success": False}), 500
