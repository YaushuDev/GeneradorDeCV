"""
Modelos de datos para el CV.
Define las estructuras de datos utilizadas en la aplicación.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Skill:
    """Representa una habilidad técnica."""
    title: str
    description: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convierte la habilidad a diccionario."""
        return {
            'title': self.title,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Skill':
        """Crea una habilidad desde un diccionario."""
        return cls(
            title=data.get('title', ''),
            description=data.get('description', '')
        )


@dataclass
class ContactInfo:
    """Información de contacto del CV."""
    email_user: Optional[str] = None
    email_domain: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    link_text: Optional[str] = None
    link_url: Optional[str] = None
    
    @property
    def full_email(self) -> Optional[str]:
        """Retorna el email completo."""
        if self.email_user and self.email_domain:
            return f"{self.email_user}@{self.email_domain}"
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la información de contacto a diccionario."""
        return {
            'emailUser': self.email_user,
            'emailDomain': self.email_domain,
            'phone': self.phone,
            'location': self.location,
            'linkText': self.link_text,
            'linkUrl': self.link_url
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContactInfo':
        """Crea información de contacto desde un diccionario."""
        return cls(
            email_user=data.get('emailUser'),
            email_domain=data.get('emailDomain'),
            phone=data.get('phone'),
            location=data.get('location'),
            link_text=data.get('linkText'),
            link_url=data.get('linkUrl')
        )


@dataclass
class CVData:
    """Modelo principal de datos del CV."""
    full_name: str = ""
    contact_info: ContactInfo = field(default_factory=ContactInfo)
    skills: List[Skill] = field(default_factory=list)
    skills_section_title: str = "TECHNICAL SKILLS"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el CV a diccionario."""
        result = {
            'fullName': self.full_name,
            'skillsSectionTitle': self.skills_section_title,
            'skills': [skill.to_dict() for skill in self.skills]
        }
        result.update(self.contact_info.to_dict())
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CVData':
        """Crea un CV desde un diccionario."""
        skills_data = data.get('skills', [])
        skills = []
        
        for skill_data in skills_data:
            if isinstance(skill_data, dict):
                skills.append(Skill.from_dict(skill_data))
            elif isinstance(skill_data, str):
                # Compatibilidad con formato antiguo
                skills.append(Skill(title='', description=skill_data))
        
        return cls(
            full_name=data.get('fullName', ''),
            contact_info=ContactInfo.from_dict(data),
            skills=skills,
            skills_section_title=data.get('skillsSectionTitle', 'TECHNICAL SKILLS')
        )
