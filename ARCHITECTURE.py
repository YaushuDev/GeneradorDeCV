"""
Diagrama de arquitectura del proyecto.
Este archivo documenta la estructura y flujo de la aplicación.
"""

# ARQUITECTURA DEL GENERADOR DE CV
# =================================

"""
┌─────────────────────────────────────────────────────────────────┐
│                         CAPA DE PRESENTACIÓN                     │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Templates   │  │    Static    │  │   Blueprints │          │
│  │   (HTML)     │  │  (CSS/JS)    │  │   (Routes)   │          │
│  └──────────────┘  └──────────────┘  └──────┬───────┘          │
│                                              │                   │
└──────────────────────────────────────────────┼───────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CAPA DE APLICACIÓN                          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      app.py                               │  │
│  │              (Application Factory)                        │  │
│  │                                                            │  │
│  │  • Crea la aplicación Flask                              │  │
│  │  • Registra blueprints                                   │  │
│  │  • Configura la aplicación                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────┬───────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CAPA DE SERVICIOS                           │
│                                                                  │
│  ┌─────────────────┐              ┌─────────────────────────┐  │
│  │  DataService    │              │     PDFService          │  │
│  │                 │              │                         │  │
│  │  • load()       │              │  ┌──────────────────┐  │  │
│  │  • save()       │              │  │ PDFStyleBuilder  │  │  │
│  │  • load_raw()   │              │  │                  │  │  │
│  │  • save_raw()   │              │  │ • get_name_style │  │  │
│  │                 │              │  │ • get_contact... │  │  │
│  └────────┬────────┘              │  └──────────────────┘  │  │
│           │                       │                         │  │
│           │                       │  ┌──────────────────┐  │  │
│           │                       │  │PDFContentBuilder │  │  │
│           │                       │  │                  │  │  │
│           │                       │  │ • build_name...  │  │  │
│           │                       │  │ • build_contact..│  │  │
│           │                       │  │ • build_skills...│  │  │
│           │                       │  └──────────────────┘  │  │
│           │                       │                         │  │
│           │                       │  • generate()           │  │
│           │                       └─────────────────────────┘  │
│           │                                                     │
└───────────┼─────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       CAPA DE MODELOS                            │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   CVData     │  │ ContactInfo  │  │    Skill     │          │
│  │              │  │              │  │              │          │
│  │ • full_name  │  │ • email_user │  │ • title      │          │
│  │ • contact_   │  │ • email_dom. │  │ • description│          │
│  │   info       │  │ • phone      │  │              │          │
│  │ • skills     │  │ • location   │  │ • to_dict()  │          │
│  │ • skills_    │  │ • link_text  │  │ • from_dict()│          │
│  │   section_   │  │ • link_url   │  │              │          │
│  │   title      │  │              │  │              │          │
│  │              │  │ • full_email │  │              │          │
│  │ • to_dict()  │  │ • to_dict()  │  │              │          │
│  │ • from_dict()│  │ • from_dict()│  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────┬───────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE CONFIGURACIÓN                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Config                                 │  │
│  │                                                            │  │
│  │  • DEBUG                                                  │  │
│  │  • CV_DATA_FILE                                           │  │
│  │  • PDF_MARGINS                                            │  │
│  │  • PDF_COLORS                                             │  │
│  │  • PDF_FONTS                                              │  │
│  │  • PDF_FONT_SIZES                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────┬───────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE PERSISTENCIA                          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  cv_data.json                             │  │
│  │                                                            │  │
│  │  {                                                        │  │
│  │    "fullName": "...",                                     │  │
│  │    "emailUser": "...",                                    │  │
│  │    "skills": [...]                                        │  │
│  │  }                                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘


FLUJO DE DATOS
==============

1. CARGAR DATOS:
   Usuario → Routes → DataService → cv_data.json → CVData Model → JSON Response

2. GUARDAR DATOS:
   Usuario → Routes → DataService → CVData Model → cv_data.json

3. GENERAR PDF:
   Usuario → Routes → PDFService → PDFStyleBuilder + PDFContentBuilder
                                 → CVData Model → PDF Buffer → Descarga


PRINCIPIOS SOLID APLICADOS
===========================

[S] Single Responsibility:
    - DataService: Solo persistencia
    - PDFService: Solo generación de PDF
    - PDFStyleBuilder: Solo estilos
    - PDFContentBuilder: Solo contenido
    - Cada Blueprint: Solo rutas específicas

[O] Open/Closed:
    - Puedes agregar nuevos servicios sin modificar existentes
    - Puedes agregar nuevas rutas con nuevos blueprints
    - Puedes extender estilos sin modificar lógica

[L] Liskov Substitution:
    - Modelos con interfaces consistentes (to_dict/from_dict)
    - Servicios intercambiables

[I] Interface Segregation:
    - PDFStyleBuilder y PDFContentBuilder separados
    - Servicios con métodos específicos

[D] Dependency Inversion:
    - Servicios reciben Config como dependencia
    - Application Factory pattern
    - Blueprints usan servicios inyectados
"""
