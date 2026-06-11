"""
Módulo de gestión de lugares para Tesoros del Barrio.
Maneja CRUD de lugares y operaciones relacionadas.
"""

from typing import Optional, List, Dict, Tuple
from datetime import datetime
import streamlit as st
from supabase import Client
from utils.supabase_client import SupabaseStorageManager, get_supabase_client


class LugaresManager:
    """
    Gestor de lugares interesantes del barrio.
    Proporciona métodos para crear, leer, actualizar y eliminar lugares.
    """
    
    CATEGORIAS = ["Parque", "Heladería", "Mural", "Mascotas", "Lugar secreto", "Otro"]
    
    @staticmethod
    def crear_lugar(
        cliente: Client,
        nombre: str,
        descripcion: str,
        categoria: str,
        latitud: float,
        longitud: float,
        autor_id: str,
        foto_url: Optional[str] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Crea un nuevo lugar en la base de datos.
        
        Args:
            cliente: Cliente de Supabase
            nombre: Nombre del lugar
            descripcion: Descripción del lugar
            categoria: Categoría del lugar
            latitud: Latitud de las coordenadas
            longitud: Longitud de las coordenadas
            autor_id: ID del usuario que crea el lugar
            foto_url: URL de la foto (opcional)
            
        Returns:
            Tupla (éxito: bool, mensaje: str, lugar_id: str|None)
        """
        try:
            # Validar datos
            if not nombre or len(nombre.strip()) == 0:
                return False, "El nombre del lugar es requerido.", None
            
            if not descripcion or len(descripcion.strip()) == 0:
                return False, "La descripción es requerida.", None
            
            if categoria not in LugaresManager.CATEGORIAS:
                return False, f"Categoría no válida. Debe ser una de: {', '.join(LugaresManager.CATEGORIAS)}", None
            
            if not (-90 <= latitud <= 90):
                return False, "Latitud no válida. Debe estar entre -90 y 90.", None
            
            if not (-180 <= longitud <= 180):
                return False, "Longitud no válida. Debe estar entre -180 y 180.", None
            
            # Crear el registro
            lugar_data = {
                "nombre": nombre.strip(),
                "descripcion": descripcion.strip(),
                "categoria": categoria,
                "latitud": latitud,
                "longitud": longitud,
                "autor_id": autor_id,
                "foto_url": foto_url
            }
            
            response = cliente.table("lugares").insert(lugar_data).execute()
            
            if response.data and len(response.data) > 0:
                lugar_id = response.data[0]["id"]
                
                # Registrar en logs de actividad
                LugaresManager._registrar_actividad(
                    cliente, autor_id, "crear_lugar",
                    f"Creó un lugar: {nombre}"
                )
                
                return True, "Lugar creado exitosamente.", lugar_id
            else:
                return False, "Error al crear el lugar. Por favor, intenta de nuevo.", None
        
        except Exception as e:
            return False, f"Error al crear lugar: {str(e)}", None
    
    @staticmethod
    def obtener_lugar(cliente: Client, lugar_id: str) -> Optional[Dict]:
        """
        Obtiene un lugar específico por su ID.
        
        Args:
            cliente: Cliente de Supabase
            lugar_id: ID del lugar
            
        Returns:
            Diccionario con datos del lugar o None
        """
        try:
            response = cliente.table("lugares").select(
                "*, usuarios:autor_id(nombre, email)"
            ).eq("id", lugar_id).single().execute()
            
            return response.data if response.data else None
        
        except Exception as e:
            print(f"Error al obtener lugar: {e}")
            return None
    
    @staticmethod
    def obtener_todos_lugares(cliente: Client) -> List[Dict]:
        """
        Obtiene todos los lugares del barrio.
        
        Args:
            cliente: Cliente de Supabase
            
        Returns:
            Lista de diccionarios con datos de lugares
        """
        try:
            response = cliente.table("lugares").select(
                "*, usuarios:autor_id(nombre, email)"
            ).order("created_at", desc=True).execute()
            
            return response.data if response.data else []
        
        except Exception as e:
            print(f"Error al obtener lugares: {e}")
            return []
    
    @staticmethod
    def obtener_lugares_usuario(cliente: Client, usuario_id: str) -> List[Dict]:
        """
        Obtiene los lugares creados por un usuario específico.
        
        Args:
            cliente: Cliente de Supabase
            usuario_id: ID del usuario
            
        Returns:
            Lista de diccionarios con datos de lugares del usuario
        """
        try:
            response = cliente.table("lugares").select("*").eq(
                "autor_id", usuario_id
            ).order("created_at", desc=True).execute()
            
            return response.data if response.data else []
        
        except Exception as e:
            print(f"Error al obtener lugares del usuario: {e}")
            return []
    
    @staticmethod
    def obtener_lugares_por_categoria(
        cliente: Client,
        categoria: str
    ) -> List[Dict]:
        """
        Obtiene lugares filtrados por categoría.
        
        Args:
            cliente: Cliente de Supabase
            categoria: Categoría a filtrar
            
        Returns:
            Lista de lugares de la categoría especificada
        """
        try:
            response = cliente.table("lugares").select(
                "*, usuarios:autor_id(nombre, email)"
            ).eq("categoria", categoria).order("created_at", desc=True).execute()
            
            return response.data if response.data else []
        
        except Exception as e:
            print(f"Error al obtener lugares por categoría: {e}")
            return []
    
    @staticmethod
    def actualizar_lugar(
        cliente: Client,
        lugar_id: str,
        usuario_id: str,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        categoria: Optional[str] = None,
        latitud: Optional[float] = None,
        longitud: Optional[float] = None,
        foto_url: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Actualiza un lugar existente.
        Solo el autor puede actualizar su lugar.
        
        Args:
            cliente: Cliente de Supabase
            lugar_id: ID del lugar a actualizar
            usuario_id: ID del usuario que intenta actualizar
            nombre: Nuevo nombre (opcional)
            descripcion: Nueva descripción (opcional)
            categoria: Nueva categoría (opcional)
            latitud: Nueva latitud (opcional)
            longitud: Nueva longitud (opcional)
            foto_url: Nueva URL de foto (opcional)
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Verificar que el usuario es el autor
            lugar = LugaresManager.obtener_lugar(cliente, lugar_id)
            
            if not lugar:
                return False, "El lugar no existe."
            
            if lugar["autor_id"] != usuario_id:
                return False, "No tienes permiso para editar este lugar."
            
            # Preparar datos a actualizar
            update_data = {}
            
            if nombre is not None and len(nombre.strip()) > 0:
                update_data["nombre"] = nombre.strip()
            
            if descripcion is not None and len(descripcion.strip()) > 0:
                update_data["descripcion"] = descripcion.strip()
            
            if categoria is not None:
                if categoria not in LugaresManager.CATEGORIAS:
                    return False, f"Categoría no válida."
                update_data["categoria"] = categoria
            
            if latitud is not None:
                if not (-90 <= latitud <= 90):
                    return False, "Latitud no válida."
                update_data["latitud"] = latitud
            
            if longitud is not None:
                if not (-180 <= longitud <= 180):
                    return False, "Longitud no válida."
                update_data["longitud"] = longitud
            
            if foto_url is not None:
                update_data["foto_url"] = foto_url
            
            if not update_data:
                return False, "No hay datos para actualizar."
            
            # Actualizar en la base de datos
            cliente.table("lugares").update(update_data).eq("id", lugar_id).execute()
            
            # Registrar en logs
            LugaresManager._registrar_actividad(
                cliente, usuario_id, "actualizar_lugar",
                f"Actualizó el lugar: {lugar['nombre']}"
            )
            
            return True, "Lugar actualizado exitosamente."
        
        except Exception as e:
            return False, f"Error al actualizar lugar: {str(e)}"
    
    @staticmethod
    def eliminar_lugar(
        cliente: Client,
        lugar_id: str,
        usuario_id: str
    ) -> Tuple[bool, str]:
        """
        Elimina un lugar de la base de datos.
        Solo el autor puede eliminar su lugar.
        
        Args:
            cliente: Cliente de Supabase
            lugar_id: ID del lugar a eliminar
            usuario_id: ID del usuario que intenta eliminar
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Verificar que el usuario es el autor
            lugar = LugaresManager.obtener_lugar(cliente, lugar_id)
            
            if not lugar:
                return False, "El lugar no existe."
            
            if lugar["autor_id"] != usuario_id:
                return False, "No tienes permiso para eliminar este lugar."
            
            # Eliminar foto del storage si existe
            if lugar.get("foto_url"):
                try:
                    # Extraer el path de la URL y eliminar
                    SupabaseStorageManager.delete_photo(cliente, lugar["foto_url"])
                except Exception as e:
                    print(f"Advertencia: No se pudo eliminar la foto: {e}")
            
            # Eliminar del lugar de la base de datos
            cliente.table("lugares").delete().eq("id", lugar_id).execute()
            
            # Registrar en logs
            LugaresManager._registrar_actividad(
                cliente, usuario_id, "eliminar_lugar",
                f"Eliminó el lugar: {lugar['nombre']}"
            )
            
            return True, "Lugar eliminado exitosamente."
        
        except Exception as e:
            return False, f"Error al eliminar lugar: {str(e)}"
    
    @staticmethod
    def _registrar_actividad(
        cliente: Client,
        usuario_id: str,
        tipo_accion: str,
        descripcion: str
    ) -> None:
        """
        Registra una actividad del usuario en la tabla de logs.
        
        Args:
            cliente: Cliente de Supabase
            usuario_id: ID del usuario
            tipo_accion: Tipo de acción realizada
            descripcion: Descripción de la acción
        """
        try:
            cliente.table("logs_actividad").insert({
                "usuario_id": usuario_id,
                "tipo_accion": tipo_accion,
                "descripcion": descripcion
            }).execute()
        except Exception as e:
            print(f"Advertencia: No se pudo registrar actividad: {e}")
