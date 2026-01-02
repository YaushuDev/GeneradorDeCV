from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

app = Flask(__name__)

CV_DATA_FILE = 'cv_data.json'

def load_data():
    if os.path.exists(CV_DATA_FILE):
        try:
            with open(CV_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data_to_file(data):
    try:
        with open(CV_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html', title="Generador de CV")

@app.route('/get_cv_data', methods=['GET'])
def get_cv_data():
    data = load_data()
    return jsonify(data)

@app.route('/save_cv_data', methods=['POST'])
def save_cv_data():
    data = request.json
    if save_data_to_file(data):
        return jsonify({"success": True})
    return jsonify({"success": False}), 500

@app.route('/perfil')
def profile():
    return render_template('page.html', title="Perfil", content="Esta es la página de perfil.")

@app.route('/configuracion')
def settings():
    return render_template('page.html', title="Configuración", content="Ajustes y preferencias aquí.")

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json
        
        # Crear un buffer en memoria para el PDF
        buffer = BytesIO()
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=36, bottomMargin=18)
        
        # Contenedor para los elementos del PDF
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para el nombre
        name_style = ParagraphStyle(
            'CustomName',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            alignment=1,  # Centrado
            fontName='Helvetica-Bold'
        )
        
        # Estilo para la información de contacto
        contact_style = ParagraphStyle(
            'ContactInfo',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            spaceAfter=8,
            alignment=1,  # Centrado
            fontName='Helvetica'
        )
        
        # Agregar nombre
        if data.get('fullName'):
            name = Paragraph(data['fullName'], name_style)
            elements.append(name)
        
        # Agregar información de contacto en una sola línea
        contact_parts = []
        
        # Email completo (usuario + dominio)
        if data.get('emailUser') and data.get('emailDomain'):
            full_email = f"{data['emailUser']}@{data['emailDomain']}"
            contact_parts.append(full_email)
        
        if data.get('phone'):
            contact_parts.append(data['phone'])
        
        if data.get('location'):
            contact_parts.append(data['location'])
        
        # Link con hipervínculo
        if data.get('linkText') and data.get('linkUrl'):
            link_html = f'<a href="{data["linkUrl"]}" color="blue">{data["linkText"]}</a>'
            contact_parts.append(link_html)
        elif data.get('linkText'):
            contact_parts.append(data['linkText'])
        
        if contact_parts:
            contact_line = " | ".join(contact_parts)
            contact_para = Paragraph(contact_line, contact_style)
            elements.append(contact_para)
        
        # Agregar línea horizontal separadora
        from reportlab.platypus import Table
        line_data = [['']]
        line_table = Table(line_data, colWidths=[6.5*inch])
        line_table.setStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#2c3e50')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ])
        elements.append(line_table)
        
        # Agregar sección de habilidades técnicas
        if data.get('skills') and len(data['skills']) > 0:
            # Estilo para el título de la sección (SIN CUADRO FEO)
            section_title_style = ParagraphStyle(
                'SectionTitle',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=12,
                fontName='Helvetica-Bold',
                alignment=0  # Alineado a la izquierda
            )
            
            # Estilo para cada línea de habilidad (título + descripción en la misma línea)
            skill_line_style = ParagraphStyle(
                'SkillLine',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#333333'),
                spaceAfter=6,
                leftIndent=0,
                fontName='Helvetica'
            )
            
            # Agregar título de la sección (personalizable)
            section_title = data.get('skillsSectionTitle', 'TECHNICAL SKILLS')
            skills_title = Paragraph(section_title, section_title_style)
            elements.append(skills_title)
            
            # Agregar cada habilidad con título y descripción en la misma línea
            for skill in data['skills']:
                if isinstance(skill, dict):
                    # Nuevo formato: con título y descripción en la misma línea
                    skill_text = ''
                    if skill.get('title'):
                        skill_text += f"<b>{skill['title']}:</b> "
                    if skill.get('description'):
                        skill_text += skill['description']
                    
                    if skill_text:
                        skill_para = Paragraph(skill_text, skill_line_style)
                        elements.append(skill_para)
                else:
                    # Formato antiguo: solo texto (para compatibilidad)
                    skill_text = f"• {skill}"
                    skill_para = Paragraph(skill_text, skill_line_style)
                    elements.append(skill_para)
            
            
            elements.append(Spacer(1, 0.3*inch))


        
        # Construir el PDF
        doc.build(elements)
        
        # Mover el puntero al inicio del buffer
        buffer.seek(0)
        
        # Enviar el PDF
        return send_file(
            buffer,
            as_attachment=True,
            download_name='mi_cv.pdf',
            mimetype='application/pdf'
        )
    
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
