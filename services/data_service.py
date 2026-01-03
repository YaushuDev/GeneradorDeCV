"""
Servicio de manejo de datos del CV.
Responsable de la persistencia y recuperación de datos.
"""
import json
import os
from typing import Dict, Any, Optional
from models.cv_data import CVData


class DataService:
    """Servicio para manejar la persistencia de datos del CV."""
    
    def __init__(self, data_file_path: str):
        """
        Inicializa el servicio de datos.
        
        Args:
            data_file_path: Ruta al archivo de datos JSON.
        """
        self.data_file_path = data_file_path
    
    def load(self) -> CVData:
        """
        Carga los datos del CV desde el archivo.
        
        Returns:
            CVData: Objeto con los datos del CV.
        """
        if os.path.exists(self.data_file_path):
            try:
                with open(self.data_file_path, 'r', encoding='utf-8') as f:
                    data_dict = json.load(f)
                    return CVData.from_dict(data_dict)
            except Exception as e:
                print(f"Error loading data: {e}")
                return CVData()
        return CVData()
    
    def load_raw(self) -> Dict[str, Any]:
        """
        Carga los datos en formato de diccionario.
        
        Returns:
            Dict: Diccionario con los datos del CV.
        """
        if os.path.exists(self.data_file_path):
            try:
                with open(self.data_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading data: {e}")
                return {}
        return {}
    
    def save(self, cv_data: CVData) -> bool:
        """
        Guarda los datos del CV en el archivo.
        
        Args:
            cv_data: Objeto CVData a guardar.
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario.
        """
        try:
            with open(self.data_file_path, 'w', encoding='utf-8') as f:
                json.dump(cv_data.to_dict(), f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def save_raw(self, data: Dict[str, Any]) -> bool:
        """
        Guarda datos en formato de diccionario.
        
        Args:
            data: Diccionario con los datos a guardar.
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario.
        """
        try:
            with open(self.data_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
