"""
Módulo de autenticación para Tesoros del Barrio.
Maneja registro, login y gestión de sesión de usuarios.
"""

import streamlit as st
from typing import Optional, Tuple
from supabase import Client
from utils.supabase_client import get_supabase_client


class AutenticacionManager:
    """
    Gestor de autenticación de usuarios.
    Proporciona métodos para registro, login y manejo de sesiones.
    """
    
    @staticmethod
    def registrar_usuario(
        email: str,
        password: str,
        nombre: str,
        client: Client
    ) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario en la aplicación.
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
            nombre: Nombre completo del usuario
            client: Cliente de Supabase
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Crear usuario en auth.users
            auth_response = client.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if auth_response.user is None:
                return False, "Error al crear el usuario. Por favor, intenta de nuevo."
            
            user_id = auth_response.user.id
            
            # Crear registro en tabla usuarios
            try:
                client.table("usuarios").insert({
                    "id": user_id,
                    "email": email,
                    "nombre": nombre
                }).execute()
                
                return True, "Registro exitoso. Por favor, inicia sesión."
            
            except Exception as e:
                # Si falla la creación en la tabla, elimina el usuario de auth
                try:
                    client.auth.admin.delete_user(user_id)
                except:
                    pass
                
                if "duplicate key" in str(e).lower() or "unique" in str(e).lower():
                    return False, "El email ya está registrado."
                return False, f"Error al registrar usuario: {str(e)}"
        
        except Exception as e:
            error_msg = str(e)
            if "already registered" in error_msg.lower():
                return False, "El email ya está registrado."
            elif "password" in error_msg.lower():
                return False, "La contraseña no es válida. Debe tener al menos 6 caracteres."
            return False, f"Error en el registro: {error_msg}"
    
    @staticmethod
    def iniciar_sesion(
        email: str,
        password: str,
        client: Client
    ) -> Tuple[bool, str, Optional[dict]]:
        """
        Inicia sesión de un usuario existente.
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
            client: Cliente de Supabase
            
        Returns:
            Tupla (éxito: bool, mensaje: str, datos_usuario: dict|None)
        """
        try:
            # Autenticar usuario
            response = client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user is None:
                return False, "Email o contraseña incorrectos.", None
            
            # Obtener datos del usuario de la tabla usuarios
            user_data = client.table("usuarios").select("*").eq(
                "id", response.user.id
            ).single().execute()
            
            usuario_info = {
                "id": response.user.id,
                "email": response.user.email,
                "nombre": user_data.data.get("nombre", ""),
                "session": response.session
            }
            
            return True, "Sesión iniciada correctamente.", usuario_info
        
        except Exception as e:
            error_msg = str(e).lower()
            if "invalid login credentials" in error_msg or "unauthorized" in error_msg:
                return False, "Email o contraseña incorrectos.", None
            return False, f"Error al iniciar sesión: {str(e)}", None
    
    @staticmethod
    def obtener_usuario_actual(client: Client) -> Optional[dict]:
        """
        Obtiene la información del usuario actualmente autenticado.
        
        Args:
            client: Cliente de Supabase
            
        Returns:
            dict con datos del usuario o None si no hay sesión
        """
        try:
            user = client.auth.get_user()
            
            if user is None or user.user is None:
                return None
            
            # Obtener datos adicionales de la tabla usuarios
            usuario_data = client.table("usuarios").select("*").eq(
                "id", user.user.id
            ).single().execute()
            
            return {
                "id": user.user.id,
                "email": user.user.email,
                "nombre": usuario_data.data.get("nombre", ""),
                **usuario_data.data
            }
        
        except Exception as e:
            return None
    
    @staticmethod
    def cerrar_sesion(client: Client) -> bool:
        """
        Cierra la sesión del usuario actual.
        
        Args:
            client: Cliente de Supabase
            
        Returns:
            bool: True si se cerró correctamente
        """
        try:
            client.auth.sign_out()
            return True
        except Exception as e:
            print(f"Error al cerrar sesión: {e}")
            return False


def inicializar_session_state():
    """
    Inicializa el state de Streamlit para manejar autenticación.
    """
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    
    if "usuario" not in st.session_state:
        st.session_state.usuario = None
    
    if "mostrar_registro" not in st.session_state:
        st.session_state.mostrar_registro = False


def verificar_autenticacion() -> Optional[dict]:
    """
    Verifica si hay un usuario autenticado.
    Si no hay sesión activa pero hay token guardado, intenta recuperar la sesión.
    
    Returns:
        dict con datos del usuario si está autenticado, None en caso contrario
    """
    inicializar_session_state()
    
    client = get_supabase_client()
    
    # Si ya está autenticado en session_state, retorna
    if st.session_state.autenticado and st.session_state.usuario:
        return st.session_state.usuario
    
    # Intenta obtener usuario actual de Supabase
    usuario_actual = AutenticacionManager.obtener_usuario_actual(client)
    
    if usuario_actual:
        st.session_state.autenticado = True
        st.session_state.usuario = usuario_actual
        return usuario_actual
    
    return None
