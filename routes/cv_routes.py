"""
Rutas relacionadas con el CV.
Maneja las peticiones HTTP para el generador de CV.
"""
from flask import Blueprint, render_template, request, jsonify, send_file
import traceback
import re
from services.data_service import DataService
from services.pdf_service import PDFService
from models.cv_data import CVData
from config.settings import Config

# Crear blueprint
cv_bp = Blueprint('cv', __name__)

# Inicializar servicios
data_service = DataService(Config.CV_DATA_FILE)
pdf_service = PDFService(Config)


@cv_bp.route('/')
def home():
    """Página principal del generador de CV."""
    return render_template('generator.html', title="Generador de CV")


@cv_bp.route('/get_cv_data', methods=['GET'])
def get_cv_data():
    """
    Obtiene los datos del CV.
    
    Returns:
        JSON con los datos del CV.
    """
    data = data_service.load_raw()
    return jsonify(data)


@cv_bp.route('/save_cv_data', methods=['POST'])
def save_cv_data():
    """
    Guarda los datos del CV.
    
    Returns:
        JSON con el resultado de la operación.
    """
    data = request.json
    if data_service.save_raw(data):
        return jsonify({"success": True})
    return jsonify({"success": False}), 500


@cv_bp.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    """
    Genera un PDF del CV.
    
    Returns:
        Archivo PDF para descargar.
    """
    try:
        data = request.json
        cv_data = CVData.from_dict(data)
        
        # Extraer font sizes si existen
        font_sizes = data.get('fontSizes', None)
        
        # Generar PDF con font sizes personalizados
        buffer = pdf_service.generate(cv_data, font_sizes)
        
        # Generar nombre del archivo
        full_name = cv_data.full_name.strip()
        if full_name:
            # Eliminar espacios y caracteres no alfanuméricos simples si se desea "todo junto"
            # El usuario pidió "ViberthEduardoCV.pdf", así que quitamos espacios.
            # También es buena práctica sanitizar un poco para evitar caracteres inválidos en nombres de archivo.
            cleaned_name = re.sub(r'[^a-zA-Z0-9]', '', full_name)
            filename = f"{cleaned_name}CV.pdf"
        else:
            filename = 'mi_cv.pdf'

        # Enviar archivo
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        print(f"Error generating PDF: {e}")
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500
