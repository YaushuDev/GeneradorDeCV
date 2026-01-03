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
from models.cv_data import CVData, Skill, EducationItem
from config.settings import Config


class PDFStyleBuilder:
    """Constructor de estilos para el PDF."""
    
    def __init__(self, config: Config, font_sizes: Dict[str, float] = None, font_family: str = "Helvetica"):
        """
        Inicializa el constructor de estilos.
        
        Args:
            config: Configuración de la aplicación.
            font_sizes: Tamaños de fuente personalizados (opcional).
            font_family: Familia de fuente global (Helvetica, Times-Roman, Courier).
        """
        self.config = config
        self.base_styles = getSampleStyleSheet()
        self.font_sizes = font_sizes or {}
        self.font_family = font_family or "Helvetica"

        # Mapping for bold and italic variants
        self.font_variants = {
            "Helvetica": {"bold": "Helvetica-Bold", "italic": "Helvetica-Oblique", "normal": "Helvetica"},
            "Times-Roman": {"bold": "Times-Bold", "italic": "Times-Italic", "normal": "Times-Roman"},
            "Courier": {"bold": "Courier-Bold", "italic": "Courier-Oblique", "normal": "Courier"},
            "Georgia": {"bold": "Times-Bold", "italic": "Times-Italic", "normal": "Times-Roman"}
        }
        # Fallback to Helvetica if unknown
        if self.font_family not in self.font_variants:
            self.font_family = "Helvetica"

    def _get_font(self, variant: str = "normal") -> str:
        """Retorna el nombre de la fuente según la variante."""
        return self.font_variants.get(self.font_family, self.font_variants["Helvetica"]).get(variant, self.font_family)
    
    def get_name_style(self) -> ParagraphStyle:
        """Retorna el estilo para el nombre."""
        # Convertir rem a puntos (1rem ≈ 12pt)
        font_size = self.font_sizes.get('name', 2.5) * 12
        return ParagraphStyle(
            'CustomName',
            parent=self.base_styles['Heading1'],
            fontSize=font_size,
            textColor=colors.HexColor(self.config.PDF_COLORS['primary']),
            spaceAfter=14,
            alignment=1,  # Centrado
            fontName=self._get_font("bold")
        )
    
    def get_contact_style(self) -> ParagraphStyle:
        """Retorna el estilo para la información de contacto."""
        font_size = self.font_sizes.get('contact', 0.9) * 12
        return ParagraphStyle(
            'ContactInfo',
            parent=self.base_styles['Normal'],
            fontSize=font_size,
            textColor=colors.HexColor(self.config.PDF_COLORS['secondary']),
            spaceAfter=10,
            alignment=1,  # Centrado
            fontName=self._get_font("normal")
        )
    
    def get_section_title_style(self) -> ParagraphStyle:
        """Retorna el estilo para títulos de sección."""
        font_size = self.font_sizes.get('sectionTitle', 1.2) * 12
        return ParagraphStyle(
            'SectionTitle',
            parent=self.base_styles['Heading2'],
            fontSize=font_size,
            textColor=colors.HexColor(self.config.PDF_COLORS['primary']),
            spaceAfter=6,
            spaceBefore=6,
            fontName=self._get_font("bold"),
            alignment=0  # Alineado a la izquierda
        )
    
    def get_skill_style(self) -> ParagraphStyle:
        """Retorna el estilo para las habilidades."""
        font_size = self.font_sizes.get('skillsContent', 0.95) * 12
        return ParagraphStyle(
            'SkillLine',
            parent=self.base_styles['Normal'],
            fontSize=font_size,
            textColor=colors.HexColor(self.config.PDF_COLORS['text']),
            spaceAfter=6,
            leftIndent=0,
            fontName=self._get_font("normal")
        )

    def get_company_style(self) -> ParagraphStyle:
        """Retorna el estilo para el nombre de la empresa."""
        font_size = self.font_sizes.get('experienceCompany', 1.0) * 12
        return ParagraphStyle(
            'CompanyName',
            parent=self.base_styles['Normal'],
            fontSize=font_size,
            textColor=colors.HexColor('#2c3e50'), # Dark Blue
            spaceAfter=2,
            fontName=self._get_font("bold")
        )

    def get_duration_style(self) -> ParagraphStyle:
        """Retorna el estilo para la duración."""
        font_size = self.font_sizes.get('experienceDuration', 0.9) * 12
        return ParagraphStyle(
            'Duration',
            parent=self.base_styles['Normal'],
            fontSize=font_size,
            textColor=colors.HexColor('#666666'),
            alignment=2, # Right aligned
            fontName=self._get_font("italic")
        )

    def get_position_style(self) -> ParagraphStyle:
        """Retorna el estilo para el puesto."""
        font_size = self.font_sizes.get('experiencePosition', 0.95) * 12
        return ParagraphStyle(
            'Position',
            parent=self.base_styles['Normal'],
            fontSize=font_size,
            textColor=colors.HexColor('#333333'),
            spaceAfter=4,
            fontName=self._get_font("bold")
        )

    def get_bullet_style(self) -> ParagraphStyle:
        """Retorna el estilo para los puntos (bullets)."""
        font_size = self.font_sizes.get('experienceBullet', 0.9) * 12
        return ParagraphStyle(
            'BulletPoint',
            parent=self.base_styles['Normal'],
            fontSize=font_size,
            textColor=colors.HexColor('#444444'),
            leftIndent=12,
            firstLineIndent=0,
            spaceAfter=6,
            fontName=self._get_font("normal")
        )


    def get_experience_left_style(self) -> ParagraphStyle:
        """Retorna el estilo para la parte izquierda de la experiencia (Empresa - Puesto)."""
        return ParagraphStyle(
            'ExpLeft',
            parent=self.base_styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            fontName=self._get_font("normal")
        )

    def get_education_institution_style(self) -> ParagraphStyle:
        """Retorna el estilo para la institución educativa."""
        font_size = self.font_sizes.get('educationInstitution', 0.95) * 12
        return ParagraphStyle(
            'EducationInstitution',
            parent=self.base_styles['Normal'],
            fontSize=font_size,
            textColor=colors.HexColor('#2c3e50'),
            fontName=self._get_font("bold")
        )

    def get_education_degree_style(self) -> ParagraphStyle:
        """Retorna el estilo para el título/grado."""
        font_size = self.font_sizes.get('educationDegree', 0.95) * 12
        return ParagraphStyle(
            'EducationDegree',
            parent=self.base_styles['Normal'],
            fontSize=font_size,
            textColor=colors.HexColor('#333333'),
            fontName=self._get_font("normal")
        )

    def get_education_date_style(self) -> ParagraphStyle:
        """Retorna el estilo para la fecha."""
        font_size = self.font_sizes.get('educationDate', 0.85) * 12
        return ParagraphStyle(
            'EducationDate',
            parent=self.base_styles['Normal'],
            fontSize=font_size,
            textColor=colors.HexColor('#666666'),
            fontName=self._get_font("italic")
        )

    def get_education_description_style(self) -> ParagraphStyle:
        """Retorna el estilo para la descripción de educación."""
        font_size = self.font_sizes.get('educationDescription', 0.9) * 12
        return ParagraphStyle(
            'EducationDescription',
            parent=self.base_styles['Normal'],
            fontSize=font_size,
            textColor=colors.HexColor('#444444'),
            leftIndent=12,
            spaceAfter=6,
            fontName=self._get_font("normal")
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
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
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
        # Ensure small spacing between skills
        skill_style.spaceAfter = 6
        
        for skill in cv_data.skills:
            skill_text = self._format_skill(skill)
            if skill_text:
                # Add bullet point to the start of each skill line
                # Ensuring it's a list item style
                # Using a table or bullet indentation could be better, but simple text prepend works for now
                full_text = f"• {skill_text}"
                skill_para = Paragraph(full_text, skill_style)
                elements.append(skill_para)
        
        elements.append(Spacer(1, 0.05*inch))
        
        return elements

    def build_education_section(self, cv_data: CVData) -> List:
        """
        Construye la sección de educación.
        
        Args:
            cv_data: Datos del CV.
            
        Returns:
            Lista de elementos para el PDF.
        """
        if not cv_data.education:
            return []
        
        elements = []
        
        # Título de la sección
        section_title_style = self.style_builder.get_section_title_style()
        edu_title = Paragraph(cv_data.education_section_title, section_title_style)
        elements.append(edu_title)
        
        # Get custom education styles
        institution_style = self.style_builder.get_education_institution_style()
        degree_style = self.style_builder.get_education_degree_style()
        date_style = self.style_builder.get_education_date_style()
        description_style = self.style_builder.get_education_description_style()
        
        # Base style for combined line
        base_font_size = self.style_builder.font_sizes.get('educationInstitution', 0.95) * 12
        combined_style = ParagraphStyle(
            'EducationCombined',
            parent=self.style_builder.base_styles['Normal'],
            fontSize=base_font_size,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=2,
            fontName=self.style_builder._get_font("normal")
        )
        
        for item in cv_data.education:
            # Line 1: Institution - Degree | Date
            # Build with inline styling to respect individual font sizes
            line1_parts = []
            
            # Get font sizes
            inst_size = self.style_builder.font_sizes.get('educationInstitution', 0.95) * 12
            deg_size = self.style_builder.font_sizes.get('educationDegree', 0.95) * 12
            date_size = self.style_builder.font_sizes.get('educationDate', 0.85) * 12
            
            if item.institution:
                line1_parts.append(f'<b><font size="{inst_size}">{item.institution}</font></b>')
            if item.degree:
                line1_parts.append(f'<font size="{deg_size}">{item.degree}</font>')
            if item.date:
                line1_parts.append(f'<i><font size="{date_size}">{item.date}</font></i>')
            
            # Join with separators " | "
            line1_text = " | ".join(line1_parts)
            
            if line1_text:
                elements.append(Paragraph(line1_text, combined_style))
                
            # Line 2: Optional description with bullet
            if item.description:
                elements.append(Paragraph(f"• {item.description}", description_style))
            
            # Spacer between items
            elements.append(Spacer(1, 0.05*inch))
        
        elements.append(Spacer(1, 0.1*inch))
        
        return elements

    def build_experience_section(self, cv_data: CVData) -> List:
        """
        Construye la sección de experiencia laboral.
        
        Args:
            cv_data: Datos del CV.
            
        Returns:
            Lista de elementos para el PDF.
        """
        if not cv_data.experience:
            return []
        
        elements = []
        
        # Título de la sección
        section_title_style = self.style_builder.get_section_title_style()
        title = Paragraph(cv_data.experience_section_title, section_title_style)
        elements.append(title)
        
        for exp in cv_data.experience:
            # Single line: Company - Position (Left) ..... Duration (Right)
            
            # Left side content: "Company - Position"
            # We use inline tags for styling
            company_text = f"<b>{exp.company}</b>"
            position_text = f"<font color='#333333'>{exp.position}</font>"
            
            # Separator
            separator = " - " if exp.position else ""
            
            left_content = f"{company_text}{separator}{position_text}"
            
            # Styles
            left_style = self.style_builder.get_experience_left_style()
            
            duration_style = self.style_builder.get_duration_style()
            
            row_data = [
                Paragraph(left_content, left_style),
                Paragraph(exp.duration, duration_style)
            ]
            
            # Table layout
            t = Table([row_data], colWidths=[5*inch, 1.5*inch])
            t.setStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ])
            elements.append(t)
            
            # Responsibilities
            if exp.responsibilities:
                bullet_style = self.style_builder.get_bullet_style()
                for resp in exp.responsibilities:
                    if resp:
                        elements.append(Paragraph(f"• {resp}", bullet_style))
            
            elements.append(Spacer(1, 0.15*inch))
            
        elements.append(Spacer(1, 0.05*inch))
        return elements
    
    def _format_skill(self, skill: Skill) -> str:
        """
        Formatea una habilidad para el PDF.
        
        Args:
            skill: Habilidad o Item de Educación a formatear.
            
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
    
    def generate(self, cv_data: CVData, font_sizes: Dict[str, float] = None) -> BytesIO:
        """
        Genera un PDF a partir de los datos del CV.
        
        Args:
            cv_data: Datos del CV.
            font_sizes: Tamaños de fuente personalizados (opcional).
            
        Returns:
            BytesIO: Buffer con el PDF generado.
        """
        # Crear style builder con font sizes personalizados
        style_builder = PDFStyleBuilder(self.config, font_sizes, cv_data.font_family)
        content_builder = PDFContentBuilder(style_builder)
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
        elements.extend(content_builder.build_name_section(cv_data.full_name))
        
        # Contacto
        elements.extend(content_builder.build_contact_section(cv_data))
        
        # Línea separadora
        elements.extend(content_builder.build_separator_line())
        
        # Habilidades
        elements.extend(content_builder.build_skills_section(cv_data))
        
        # Experiencia
        elements.extend(content_builder.build_experience_section(cv_data))
        
        # Educación
        elements.extend(content_builder.build_education_section(cv_data))
        
        # Construir PDF
        doc.build(elements)
        
        # Resetear buffer
        buffer.seek(0)
        
        return buffer
