"""
Aplicación principal del Generador de CV.
Punto de entrada de la aplicación Flask.
"""
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


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)
