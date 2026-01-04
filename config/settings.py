"""
Configuración de la aplicación.
Centraliza todas las configuraciones para facilitar el mantenimiento.
"""
import os
import sys

class Config:
    """Configuración base de la aplicación."""
    
    # Configuración de Flask
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuración de archivos
    # Detectar si estamos ejecutando desde PyInstaller
    if getattr(sys, 'frozen', False):
        # Si está empaquetado, usar el directorio del ejecutable
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        # Si está en desarrollo, usar el directorio del proyecto
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    CV_DATA_FILE = os.path.join(BASE_DIR, 'cv_data.json')
    PROMPTS_DATA_FILE = os.path.join(BASE_DIR, 'prompts_data.json')
    
    # Configuración de PDF
    PDF_PAGE_SIZE = 'letter'
    PDF_MARGINS = {
        'right': 72,
        'left': 72,
        'top': 18,
        'bottom': 18
    }
    
    # Configuración de estilos PDF
    PDF_COLORS = {
        'primary': '#2c3e50',
        'secondary': '#555555',
        'text': '#333333'
    }
    
    PDF_FONTS = {
        'name': 'Helvetica-Bold',
        'contact': 'Helvetica',
        'section_title': 'Helvetica-Bold',
        'skill': 'Helvetica'
    }
    
    PDF_FONT_SIZES = {
        'name': 28,
        'contact': 10,
        'section_title': 14,
        'skill': 11
    }


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False


# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
