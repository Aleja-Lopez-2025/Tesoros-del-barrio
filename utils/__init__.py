"""
Paquete de utilidades para Tesoros del Barrio.
Contiene módulos para autenticación, gestión de lugares y cliente de Supabase.
"""

from utils.supabase_client import get_supabase_client, SupabaseStorageManager, verificar_conexion
from utils.auth import AutenticacionManager, verificar_autenticacion, inicializar_session_state
from utils.places import LugaresManager

__all__ = [
    "get_supabase_client",
    "SupabaseStorageManager",
    "verificar_conexion",
    "AutenticacionManager",
    "verificar_autenticacion",
    "inicializar_session_state",
    "LugaresManager",
]
