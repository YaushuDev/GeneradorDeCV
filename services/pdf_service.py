"""
Servicio de generación de PDF.
Responsable de crear documentos PDF a partir de los datos del CV.
"""
from io import BytesIO
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from models.cv_data import CVData, Skill
from config.settings import Config


class PDFStyleBuilder:
    """Constructor de estilos para el PDF."""
    
    def __init__(self, config: Config):
        """
        Inicializa el constructor de estilos.
        
        Args:
            config: Configuración de la aplicación.
        """
        self.config = config
        self.base_styles = getSampleStyleSheet()
    
    def get_name_style(self) -> ParagraphStyle:
        """Retorna el estilo para el nombre."""
        return ParagraphStyle(
            'CustomName',
            parent=self.base_styles['Heading1'],
            fontSize=self.config.PDF_FONT_SIZES['name'],
            textColor=colors.HexColor(self.config.PDF_COLORS['primary']),
            spaceAfter=12,
            alignment=1,  # Centrado
            fontName=self.config.PDF_FONTS['name']
        )
    
    def get_contact_style(self) -> ParagraphStyle:
        """Retorna el estilo para la información de contacto."""
        return ParagraphStyle(
            'ContactInfo',
            parent=self.base_styles['Normal'],
            fontSize=self.config.PDF_FONT_SIZES['contact'],
            textColor=colors.HexColor(self.config.PDF_COLORS['secondary']),
            spaceAfter=8,
            alignment=1,  # Centrado
            fontName=self.config.PDF_FONTS['contact']
        )
    
    def get_section_title_style(self) -> ParagraphStyle:
        """Retorna el estilo para títulos de sección."""
        return ParagraphStyle(
            'SectionTitle',
            parent=self.base_styles['Heading2'],
            fontSize=self.config.PDF_FONT_SIZES['section_title'],
            textColor=colors.HexColor(self.config.PDF_COLORS['primary']),
            spaceAfter=12,
            fontName=self.config.PDF_FONTS['section_title'],
            alignment=0  # Alineado a la izquierda
        )
    
    def get_skill_style(self) -> ParagraphStyle:
        """Retorna el estilo para las habilidades."""
        return ParagraphStyle(
            'SkillLine',
            parent=self.base_styles['Normal'],
            fontSize=self.config.PDF_FONT_SIZES['skill'],
            textColor=colors.HexColor(self.config.PDF_COLORS['text']),
            spaceAfter=6,
            leftIndent=0,
            fontName=self.config.PDF_FONTS['skill']
        )


class PDFContentBuilder:
    """Constructor de contenido para el PDF."""
    
    def __init__(self, style_builder: PDFStyleBuilder):
        """
        Inicializa el constructor de contenido.
        
        Args:
            style_builder: Constructor de estilos.
        """
        self.style_builder = style_builder
    
    def build_name_section(self, full_name: str) -> List:
        """
        Construye la sección del nombre.
        
        Args:
            full_name: Nombre completo.
            
        Returns:
            Lista de elementos para el PDF.
        """
        if not full_name:
            return []
        
        name_style = self.style_builder.get_name_style()
        return [Paragraph(full_name, name_style)]
    
    def build_contact_section(self, cv_data: CVData) -> List:
        """
        Construye la sección de contacto.
        
        Args:
            cv_data: Datos del CV.
            
        Returns:
            Lista de elementos para el PDF.
        """
        contact_parts = []
        contact_info = cv_data.contact_info
        
        # Email completo
        if contact_info.full_email:
            contact_parts.append(contact_info.full_email)
        
        if contact_info.phone:
            contact_parts.append(contact_info.phone)
        
        if contact_info.location:
            contact_parts.append(contact_info.location)
        
        # Link con hipervínculo
        if contact_info.link_text and contact_info.link_url:
            link_html = f'<a href="{contact_info.link_url}" color="blue">{contact_info.link_text}</a>'
            contact_parts.append(link_html)
        elif contact_info.link_text:
            contact_parts.append(contact_info.link_text)
        
        if not contact_parts:
            return []
        
        contact_style = self.style_builder.get_contact_style()
        contact_line = " | ".join(contact_parts)
        return [Paragraph(contact_line, contact_style)]
    
    def build_separator_line(self) -> List:
        """
        Construye una línea separadora horizontal.
        
        Returns:
            Lista de elementos para el PDF.
        """
        line_data = [['']]
        line_table = Table(line_data, colWidths=[6.5*inch])
        line_table.setStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#2c3e50')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ])
        return [line_table]
    
    def build_skills_section(self, cv_data: CVData) -> List:
        """
        Construye la sección de habilidades técnicas.
        
        Args:
            cv_data: Datos del CV.
            
        Returns:
            Lista de elementos para el PDF.
        """
        if not cv_data.skills:
            return []
        
        elements = []
        
        # Título de la sección
        section_title_style = self.style_builder.get_section_title_style()
        skills_title = Paragraph(cv_data.skills_section_title, section_title_style)
        elements.append(skills_title)
        
        # Habilidades
        skill_style = self.style_builder.get_skill_style()
        for skill in cv_data.skills:
            skill_text = self._format_skill(skill)
            if skill_text:
                skill_para = Paragraph(skill_text, skill_style)
                elements.append(skill_para)
        
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _format_skill(self, skill: Skill) -> str:
        """
        Formatea una habilidad para el PDF.
        
        Args:
            skill: Habilidad a formatear.
            
        Returns:
            Texto formateado de la habilidad.
        """
        skill_text = ''
        if skill.title:
            skill_text += f"<b>{skill.title}:</b> "
        if skill.description:
            skill_text += skill.description
        return skill_text


class PDFService:
    """Servicio principal para la generación de PDFs."""
    
    def __init__(self, config: Config):
        """
        Inicializa el servicio de PDF.
        
        Args:
            config: Configuración de la aplicación.
        """
        self.config = config
        self.style_builder = PDFStyleBuilder(config)
        self.content_builder = PDFContentBuilder(self.style_builder)
    
    def generate(self, cv_data: CVData) -> BytesIO:
        """
        Genera un PDF a partir de los datos del CV.
        
        Args:
            cv_data: Datos del CV.
            
        Returns:
            BytesIO: Buffer con el PDF generado.
        """
        buffer = BytesIO()
        
        # Crear documento
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=self.config.PDF_MARGINS['right'],
            leftMargin=self.config.PDF_MARGINS['left'],
            topMargin=self.config.PDF_MARGINS['top'],
            bottomMargin=self.config.PDF_MARGINS['bottom']
        )
        
        # Construir elementos
        elements = []
        
        # Nombre
        elements.extend(self.content_builder.build_name_section(cv_data.full_name))
        
        # Contacto
        elements.extend(self.content_builder.build_contact_section(cv_data))
        
        # Línea separadora
        elements.extend(self.content_builder.build_separator_line())
        
        # Habilidades
        elements.extend(self.content_builder.build_skills_section(cv_data))
        
        # Construir PDF
        doc.build(elements)
        
        # Resetear buffer
        buffer.seek(0)
        
        return buffer
