"""
Cliente de Supabase reutilizable para Tesoros del Barrio.
Proporciona funciones para interactuar con la base de datos y storage.
"""

import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Variables de entorno (pueden ser None si no están configuradas)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client() -> Client:
    """
    Obtiene el cliente de Supabase inicializado.
    
    Returns:
        Client: Cliente de Supabase conectado
    
    Raises:
        ValueError: Si falta alguna variable de entorno
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "❌ ERROR: Variables de entorno faltantes\n\n"
            "Necesitas configurar estas variables en Streamlit Cloud:\n"
            "• SUPABASE_URL\n"
            "• SUPABASE_KEY\n\n"
            "Pasos:\n"
            "1. Ve a tu app en Streamlit Cloud\n"
            "2. Haz clic en 'Manage app' (arriba a la derecha)\n"
            "3. Ve a la sección 'Secrets'\n"
            "4. Añade tus claves de Supabase\n"
            "5. Haz clic en 'Save'"
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def verificar_conexion() -> bool:
    """
    Verifica la conexión con Supabase.
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        client = get_supabase_client()
        # Intenta hacer una consulta simple
        response = client.table("usuarios").select("count", count="exact").limit(1).execute()
        return True
    except Exception as e:
        print(f"Error al verificar conexión con Supabase: {e}")
        return False


class SupabaseStorageManager:
    """
    Gestor para operaciones con Supabase Storage.
    Maneja carga y descarga de archivos.
    """
    
    BUCKET_NAME = "lugares-fotos"
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    
    @staticmethod
    def init_bucket(client: Client) -> bool:
        """
        Inicializa el bucket de almacenamiento si no existe.
        
        Args:
            client: Cliente de Supabase
            
        Returns:
            bool: True si se inicializó correctamente
        """
        try:
            # Intenta obtener información del bucket
            client.storage.get_bucket(SupabaseStorageManager.BUCKET_NAME)
            return True
        except Exception:
            try:
                # Si no existe, crea el bucket
                client.storage.create_bucket(
                    SupabaseStorageManager.BUCKET_NAME,
                    options={"public": True}
                )
                return True
            except Exception as e:
                print(f"Error inicializando bucket: {e}")
                return False
    
    @staticmethod
    def upload_photo(
        client: Client,
        file_bytes: bytes,
        file_name: str,
        usuario_id: str
    ) -> Optional[str]:
        """
        Carga una foto a Supabase Storage.
        
        Args:
            client: Cliente de Supabase
            file_bytes: Contenido del archivo en bytes
            file_name: Nombre del archivo
            usuario_id: ID del usuario que carga el archivo
            
        Returns:
            str: URL pública del archivo cargado, None si hay error
        """
        try:
            # Validar tamaño del archivo
            if len(file_bytes) > SupabaseStorageManager.MAX_FILE_SIZE:
                print(f"Archivo demasiado grande. Máximo: {SupabaseStorageManager.MAX_FILE_SIZE} bytes")
                return None
            
            # Validar extensión
            import os
            _, ext = os.path.splitext(file_name)
            if ext.lower() not in SupabaseStorageManager.ALLOWED_EXTENSIONS:
                print(f"Extensión de archivo no permitida. Permitidas: {SupabaseStorageManager.ALLOWED_EXTENSIONS}")
                return None
            
            # Crear ruta única: usuario_id/timestamp_filename
            import time
            timestamp = int(time.time() * 1000)
            remote_path = f"{usuario_id}/{timestamp}_{file_name}"
            
            # Subir archivo
            response = client.storage.from_(SupabaseStorageManager.BUCKET_NAME).upload(
                remote_path,
                file_bytes
            )
            
            # Construir URL pública
            url = client.storage.from_(SupabaseStorageManager.BUCKET_NAME).get_public_url(remote_path)
            return url
        
        except Exception as e:
            print(f"Error al subir foto: {e}")
            return None
    
    @staticmethod
    def delete_photo(client: Client, file_path: str) -> bool:
        """
        Elimina una foto de Supabase Storage.
        
        Args:
            client: Cliente de Supabase
            file_path: Ruta del archivo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            client.storage.from_(SupabaseStorageManager.BUCKET_NAME).remove([file_path])
            return True
        except Exception as e:
            print(f"Error al eliminar foto: {e}")
            return False
    
    @staticmethod
    def get_public_url(file_path: str) -> str:
        """
        Obtiene la URL pública de un archivo en el bucket.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            str: URL pública del archivo
        """
        client = get_supabase_client()
        return client.storage.from_(SupabaseStorageManager.BUCKET_NAME).get_public_url(file_path)
