"""
Aplicación principal del Generador de CV.
Punto de entrada de la aplicación Flask.
"""
import webbrowser
import threading
from flask import Flask
from config import config
from routes import cv_bp, general_bp


def create_app(config_name='default'):
    """
    Factory function para crear la aplicación Flask.
    
    Args:
        config_name: Nombre de la configuración a usar ('development', 'production', 'default').
        
    Returns:
        Flask: Instancia de la aplicación Flask configurada.
    """
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Registrar blueprints
    app.register_blueprint(cv_bp)
    app.register_blueprint(general_bp)
    
    return app


def open_browser():
    """
    Abre el navegador automáticamente después de un pequeño delay.
    """
    import time
    time.sleep(1.5)  # Esperar a que el servidor esté listo
    webbrowser.open('http://localhost:5000')


if __name__ == '__main__':
    app = create_app('production')  # Usar producción para evitar reloader
    
    # Solo abrir el navegador si no es el proceso de recarga de Flask
    # WERKZEUG_RUN_MAIN es None en el proceso principal
    import os
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(debug=False, use_reloader=False)  # Desactivar debug y reloader
