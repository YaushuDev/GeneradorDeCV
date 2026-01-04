# Instrucciones de Uso del Ejecutable GeneradorCV

## 📦 Ubicación del Ejecutable
El ejecutable se encuentra en: `dist\GeneradorCV.exe`

## 🚀 Cómo Usar

### Primera Ejecución
1. Copia `GeneradorCV.exe` a cualquier carpeta de tu preferencia
2. Haz doble clic en `GeneradorCV.exe`
3. El navegador se abrirá automáticamente en `http://localhost:5000`
4. Se creará automáticamente un archivo `cv_data.json` en la misma carpeta donde está el ejecutable

### Ejecuciones Posteriores
1. Haz doble clic en `GeneradorCV.exe`
2. La aplicación cargará automáticamente los datos guardados del archivo `cv_data.json`
3. Todos tus cambios se guardarán en el mismo archivo JSON

## 📁 Gestión de Datos

### Archivo cv_data.json
- **Ubicación**: Se crea en el mismo directorio donde está `GeneradorCV.exe`
- **Creación**: Automática en la primera ejecución
- **Persistencia**: Los datos se guardan automáticamente al hacer cambios
- **Portabilidad**: Puedes copiar tanto el `.exe` como el `.json` a otra ubicación

### Ejemplo de Estructura de Carpetas
```
MiCarpetaCV/
├── GeneradorCV.exe          (Ejecutable)
└── cv_data.json            (Datos guardados - se crea automáticamente)
```

## ✅ Características del Ejecutable

- ✅ No requiere Python instalado
- ✅ No requiere instalación
- ✅ Abre el navegador automáticamente (solo una vez)
- ✅ Gestión automática del archivo de datos
- ✅ Portátil - puedes moverlo a cualquier carpeta
- ✅ Todos los datos se guardan localmente

## 🔧 Solución de Problemas

### El navegador no se abre automáticamente
- Abre manualmente tu navegador y ve a `http://localhost:5000`

### No puedo guardar los datos
- Verifica que tengas permisos de escritura en la carpeta donde está el ejecutable
- El archivo `cv_data.json` debe poder crearse/modificarse

### Quiero empezar de cero
- Simplemente elimina el archivo `cv_data.json`
- Al ejecutar nuevamente, se creará uno nuevo vacío

## 📝 Notas Importantes

1. **Una instancia a la vez**: Solo ejecuta una copia del programa a la vez
2. **Puerto 5000**: El programa usa el puerto 5000, asegúrate de que esté disponible
3. **Datos locales**: Todos los datos se guardan localmente en `cv_data.json`
4. **Respaldo**: Haz copias de seguridad de `cv_data.json` si tienes datos importantes
