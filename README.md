# Generador de CV

Aplicación Flask para generar CVs profesionales en formato PDF.

## 🏗️ Arquitectura del Proyecto

El proyecto ha sido refactorizado siguiendo los principios **SOLID** para mejorar la mantenibilidad, escalabilidad y testabilidad del código.

### Estructura de Directorios

```
GeneradorDeCV/
├── config/              # Configuración de la aplicación
│   ├── __init__.py
│   └── settings.py      # Configuraciones centralizadas
├── models/              # Modelos de datos
│   ├── __init__.py
│   └── cv_data.py       # Modelos: CVData, ContactInfo, Skill
├── services/            # Lógica de negocio
│   ├── __init__.py
│   ├── data_service.py  # Persistencia de datos
│   └── pdf_service.py   # Generación de PDFs
├── routes/              # Rutas de Flask (Blueprints)
│   ├── __init__.py
│   ├── cv_routes.py     # Rutas del CV
│   └── general_routes.py # Rutas generales
├── templates/           # Plantillas HTML
├── static/              # Archivos estáticos (CSS, JS, imágenes)
├── app.py               # Punto de entrada de la aplicación
├── cv_data.json         # Almacenamiento de datos del CV
└── requirements.txt     # Dependencias
```

## 🎯 Principios SOLID Aplicados

### 1. **Single Responsibility Principle (SRP)**
Cada clase/módulo tiene una única responsabilidad:
- `DataService`: Solo maneja la persistencia de datos
- `PDFService`: Solo genera PDFs
- `PDFStyleBuilder`: Solo construye estilos para PDFs
- `PDFContentBuilder`: Solo construye contenido para PDFs
- Blueprints: Solo manejan rutas HTTP

### 2. **Open/Closed Principle (OCP)**
El código está abierto a extensión pero cerrado a modificación:
- Puedes agregar nuevos servicios sin modificar los existentes
- Puedes agregar nuevas rutas creando nuevos blueprints
- Puedes extender los estilos del PDF sin modificar la lógica existente

### 3. **Liskov Substitution Principle (LSP)**
Las clases pueden ser sustituidas por sus subclases sin romper la funcionalidad:
- Los modelos de datos usan interfaces claras (`to_dict`, `from_dict`)
- Los servicios tienen contratos bien definidos

### 4. **Interface Segregation Principle (ISP)**
Interfaces específicas en lugar de interfaces generales:
- `PDFStyleBuilder` y `PDFContentBuilder` están separados
- Cada servicio expone solo los métodos necesarios

### 5. **Dependency Inversion Principle (DIP)**
Dependencias a través de abstracciones:
- Los servicios reciben configuración como parámetro
- Los blueprints usan servicios inyectados
- Uso del patrón Application Factory

## 🚀 Instalación y Uso

### Requisitos
- Python 3.8+
- pip

### Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
```bash
python -m venv .venv
```

3. Activar el entorno virtual:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Ejecutar la Aplicación

```bash
python app.py
```

O usar el script de inicio:
```bash
run.bat
```

La aplicación estará disponible en `http://localhost:5000`

### 📦 Generar Ejecutable con PyInstaller

Para crear un ejecutable independiente de la aplicación:

1. Asegúrate de tener PyInstaller instalado:
```bash
pip install pyinstaller
```

2. Genera el ejecutable con el siguiente comando:
```bash
.venv\Scripts\pyinstaller.exe --name="GeneradorCV" --onefile --windowed --add-data "templates;templates" --add-data "static;static" --add-data "config;config" --add-data "models;models" --add-data "services;services" --add-data "routes;routes" app.py
```

**Parámetros explicados:**
- `--name="GeneradorCV"`: Nombre del ejecutable
- `--onefile`: Crea un único archivo ejecutable
- `--windowed`: No muestra la consola (solo la aplicación web)
- `--add-data`: Incluye carpetas necesarias (templates, static, etc.)
- `--icon`: Ícono del ejecutable (opcional)

3. El ejecutable se generará en la carpeta `dist/`

4. Para ejecutar, simplemente haz doble clic en `GeneradorCV.exe`

**Nota:** 
- La aplicación abrirá automáticamente tu navegador predeterminado al ejecutarse.
- El archivo `cv_data.json` se creará automáticamente en el mismo directorio donde se encuentra el ejecutable.
- Si el archivo JSON ya existe, la aplicación cargará los datos guardados anteriormente.

### 🔨 Script Rápido para Generar Ejecutable

También puedes crear un archivo `build.bat` con el siguiente contenido:

```batch
@echo off
echo Generando ejecutable...
.venv\Scripts\pyinstaller.exe --name="GeneradorCV" --onefile --windowed --add-data "templates;templates" --add-data "static;static" --add-data "config;config" --add-data "models;models" --add-data "services;services" --add-data "routes;routes" app.py
echo.
echo Ejecutable generado en la carpeta dist/
pause
```

Luego solo ejecuta `build.bat` para generar el ejecutable automáticamente.

## 📝 Características

- ✅ Editor de CV con interfaz intuitiva
- ✅ Generación de PDF profesional
- ✅ Persistencia de datos en JSON
- ✅ Modo claro/oscuro
- ✅ Diseño responsive
- ✅ Secciones personalizables:
  - Información personal
  - Datos de contacto
  - Habilidades técnicas

## 🔧 Configuración

La configuración se encuentra en `config/settings.py`. Puedes modificar:
- Colores del PDF
- Tamaños de fuente
- Márgenes del documento
- Rutas de archivos

## 🧪 Testing

La estructura modular facilita la creación de tests unitarios:

```python
# Ejemplo de test para DataService
from services.data_service import DataService
from models.cv_data import CVData

def test_save_and_load():
    service = DataService('test_data.json')
    cv_data = CVData(full_name="Test User")
    
    assert service.save(cv_data) == True
    loaded_data = service.load()
    assert loaded_data.full_name == "Test User"
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 🎨 Mejoras Futuras

- [ ] Tests unitarios y de integración
- [ ] Más secciones del CV (experiencia laboral, educación, etc.)
- [ ] Múltiples plantillas de diseño
- [ ] Exportación a otros formatos (Word, HTML)
- [ ] Autenticación de usuarios
- [ ] Base de datos SQL en lugar de JSON
