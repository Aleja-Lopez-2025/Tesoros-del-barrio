"""
Tesoros del Barrio - Aplicación Web Colaborativa
=====================================

Una aplicación web moderna y colaborativa que permite a niños y amigos
descubrir y compartir lugares interesantes de su vecindario mediante
un mapa interactivo.

Tecnologías:
- Python 3.8+
- Streamlit (framework web)
- Supabase (base de datos y autenticación)
- Folium (mapas interactivos)
- Streamlit-Folium (integración de mapas)

Autor: Desarrollador Senior
Fecha: 2024
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime
import json
from typing import Optional, Dict, List
from PIL import Image
import io

# Importaciones locales
from utils.supabase_client import get_supabase_client, SupabaseStorageManager, verificar_conexion
from utils.auth import AutenticacionManager, verificar_autenticacion, inicializar_session_state
from utils.places import LugaresManager

# ==========================================
# CONFIGURACIÓN INICIAL DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Tesoros del Barrio",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔐 VALIDACIÓN CRÍTICA: Verificar variables de entorno
import os
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Debug: mostrar si las variables existen (sin mostrar los valores reales)
debug_url_exists = bool(SUPABASE_URL)
debug_key_exists = bool(SUPABASE_KEY)

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error(f"""
    # 🔴 Error de Configuración - Variables de Entorno Faltantes
    
    ### Estado Actual:
    - SUPABASE_URL configurado: **{"✅ SÍ" if debug_url_exists else "❌ NO"}**
    - SUPABASE_KEY configurado: **{"✅ SÍ" if debug_key_exists else "❌ NO"}**
    
    ### Solución:
    
    **En Streamlit Cloud:**
    1. Ve a tu app → Click en **⋮** (arriba a la derecha)
    2. Selecciona **"Manage app"**
    3. Ve a **Settings → Secrets**
    4. Agrega esto (reemplaza con TUS valores reales):
    ```
    SUPABASE_URL = "https://tuproyecto.supabase.co"
    SUPABASE_KEY = "tu-anon-key-aqui"
    ```
    5. Haz click en **Save**
    6. **ESPERA 1-2 MINUTOS** a que la app se redeploy automáticamente
    
    **Si lo hiciste correctamente pero aún ves este error:**
    - Haz click en **⋮ → Reboot app**
    - Espera 30 segundos
    - Recarga la página en tu navegador (F5 o Cmd+R)
    """)
    st.stop()

# Inicializar session state
inicializar_session_state()

# CSS personalizado para mejor diseño
st.markdown("""
<style>
    /* Color principal: verde bosque */
    :root {
        --primary-color: #2d7d4d;
        --secondary-color: #f0ad4e;
        --danger-color: #d9534f;
        --success-color: #5cb85c;
    }
    
    .main {
        padding: 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .lugar-card {
        background: white;
        border-left: 4px solid #2d7d4d;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .categoria-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        margin: 5px 5px 5px 0;
    }
    
    .categoria-parque { background-color: #90EE90; color: black; }
    .categoria-heladeria { background-color: #FFB6C1; color: black; }
    .categoria-mural { background-color: #87CEEB; color: black; }
    .categoria-mascotas { background-color: #FFD700; color: black; }
    .categoria-secreto { background-color: #DDA0DD; color: black; }
    .categoria-otro { background-color: #D3D3D3; color: black; }
    
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 30px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        text-align: center;
        color: #2d7d4d;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    
    .header-subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1em;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def get_categoria_color(categoria: str) -> str:
    """
    Retorna el color de un marcador basado en su categoría.
    
    Args:
        categoria: Nombre de la categoría
        
    Returns:
        Color en formato hexadecimal
    """
    colores = {
        "Parque": "#90EE90",
        "Heladería": "#FFB6C1",
        "Mural": "#87CEEB",
        "Mascotas": "#FFD700",
        "Lugar secreto": "#DDA0DD",
        "Otro": "#D3D3D3"
    }
    return colores.get(categoria, "#808080")


def get_categoria_icon(categoria: str) -> str:
    """
    Retorna un emoji representativo de la categoría.
    
    Args:
        categoria: Nombre de la categoría
        
    Returns:
        Emoji como string
    """
    iconos = {
        "Parque": "🌳",
        "Heladería": "🍦",
        "Mural": "🎨",
        "Mascotas": "🐾",
        "Lugar secreto": "🔐",
        "Otro": "📍"
    }
    return iconos.get(categoria, "📍")


def crear_mapa(lugares: List[Dict], centro_lat: float = 4.7110, centro_lon: float = -74.0055) -> folium.Map:
    """
    Crea un mapa interactivo de Folium con los lugares marcados.
    
    Args:
        lugares: Lista de lugares a mostrar en el mapa
        centro_lat: Latitud del centro del mapa (por defecto Bogotá)
        centro_lon: Longitud del centro del mapa (por defecto Bogotá)
        
    Returns:
        Objeto Map de Folium
    """
    # Crear mapa centrado
    mapa = folium.Map(
        location=[centro_lat, centro_lon],
        zoom_start=12,
        tiles="OpenStreetMap"
    )
    
    # Agregar marcadores para cada lugar
    for lugar in lugares:
        try:
            coordenadas = [lugar["latitud"], lugar["longitud"]]
            
            # Crear popup con información del lugar
            popup_html = f"""
            <div style="width: 300px; font-family: Arial;">
                <h4>{lugar['nombre']}</h4>
                <p><strong>Categoría:</strong> {lugar['categoria']}</p>
                <p><strong>Descripción:</strong> {lugar['descripcion']}</p>
                <p><strong>Autor:</strong> {lugar['usuarios']['nombre']}</p>
                <p><strong>Fecha:</strong> {lugar['created_at'][:10]}</p>
                <hr>
                <p><small>Lat: {lugar['latitud']:.6f}, Lon: {lugar['longitud']:.6f}</small></p>
            </div>
            """
            
            folium.Marker(
                location=coordenadas,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=lugar["nombre"],
                icon=folium.Icon(
                    color="green" if lugar["categoria"] == "Parque" else
                    "pink" if lugar["categoria"] == "Heladería" else
                    "blue" if lugar["categoria"] == "Mural" else
                    "orange" if lugar["categoria"] == "Mascotas" else
                    "purple" if lugar["categoria"] == "Lugar secreto" else
                    "gray",
                    icon="info-sign"
                )
            ).add_to(mapa)
        
        except Exception as e:
            print(f"Error al agregar marcador: {e}")
            continue
    
    return mapa


def mostrar_card_lugar(lugar: Dict, usuario_actual: Optional[Dict] = None):
    """
    Muestra una tarjeta con la información de un lugar.
    
    Args:
        lugar: Diccionario con datos del lugar
        usuario_actual: Datos del usuario autenticado (para mostrar opciones de edición)
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div class="lugar-card">
            <h4>{get_categoria_icon(lugar['categoria'])} {lugar['nombre']}</h4>
            <span class="categoria-badge categoria-{lugar['categoria'].lower().replace(' ', '-')}">{lugar['categoria']}</span>
            <p><strong>Descripción:</strong> {lugar['descripcion']}</p>
            <p><strong>📍 Ubicación:</strong> ({lugar['latitud']:.4f}, {lugar['longitud']:.4f})</p>
            <p><strong>👤 Autor:</strong> {lugar['usuarios']['nombre']}</p>
            <p><strong>📅 Fecha:</strong> {lugar['created_at'][:10]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar foto si existe
        if lugar.get("foto_url"):
            try:
                st.image(lugar["foto_url"], width=200, caption="Foto del lugar")
            except Exception as e:
                st.warning("No se pudo cargar la imagen")
    
    # Botones de acción si es el propietario
    if usuario_actual and usuario_actual["id"] == lugar["autor_id"]:
        with col2:
            if st.button("✏️ Editar", key=f"edit_{lugar['id']}"):
                st.session_state.editar_lugar_id = lugar["id"]
            
            if st.button("🗑️ Eliminar", key=f"delete_{lugar['id']}", help="Esta acción no se puede deshacer"):
                st.session_state.confirmar_eliminar_id = lugar["id"]


# ==========================================
# INTERFAZ DE AUTENTICACIÓN
# ==========================================

def pantalla_autenticacion():
    """
    Muestra la pantalla de autenticación (login/registro).
    """
    st.markdown("<div class='header-title'>🗺️ Tesoros del Barrio</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-subtitle'>Descubre y comparte lugares increíbles de tu barrio</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
        
        # Toggle entre login y registro
        tab1, tab2 = st.tabs(["Iniciar Sesión", "Registro"])
        
        with tab1:
            st.subheader("🔓 Iniciar Sesión")
            
            email_login = st.text_input(
                "Email",
                key="login_email",
                placeholder="tu@email.com"
            )
            
            password_login = st.text_input(
                "Contraseña",
                type="password",
                key="login_password",
                placeholder="••••••"
            )
            
            if st.button("Entrar", use_container_width=True, type="primary"):
                if not email_login or not password_login:
                    st.error("Por favor completa todos los campos")
                else:
                    try:
                        client = get_supabase_client()
                        success, message, usuario_info = AutenticacionManager.iniciar_sesion(
                            email_login,
                            password_login,
                            client
                        )
                        
                        if success:
                            st.session_state.autenticado = True
                            st.session_state.usuario = usuario_info
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with tab2:
            st.subheader("📝 Crear Cuenta")
            
            nombre_registro = st.text_input(
                "Nombre completo",
                key="registro_nombre",
                placeholder="Tu nombre"
            )
            
            email_registro = st.text_input(
                "Email",
                key="registro_email",
                placeholder="tu@email.com"
            )
            
            password_registro = st.text_input(
                "Contraseña",
                type="password",
                key="registro_password",
                placeholder="Mínimo 6 caracteres"
            )
            
            password_confirm = st.text_input(
                "Confirmar contraseña",
                type="password",
                key="registro_password_confirm",
                placeholder="Confirma tu contraseña"
            )
            
            if st.button("Registrarse", use_container_width=True, type="primary"):
                # Validación básica
                if not all([nombre_registro, email_registro, password_registro, password_confirm]):
                    st.error("Por favor completa todos los campos")
                elif password_registro != password_confirm:
                    st.error("Las contraseñas no coinciden")
                elif len(password_registro) < 6:
                    st.error("La contraseña debe tener al menos 6 caracteres")
                else:
                    try:
                        client = get_supabase_client()
                        success, message = AutenticacionManager.registrar_usuario(
                            email_registro,
                            password_registro,
                            nombre_registro,
                            client
                        )
                        
                        if success:
                            st.success(message)
                            st.info("Puedes iniciar sesión con tus credenciales en la pestaña 'Iniciar Sesión'")
                        else:
                            st.error(message)
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# INTERFAZ PRINCIPAL (CON USUARIO AUTENTICADO)
# ==========================================

def pantalla_principal(usuario: Dict):
    """
    Muestra la pantalla principal de la aplicación con el mapa y gestión de lugares.
    
    Args:
        usuario: Diccionario con datos del usuario autenticado
    """
    client = get_supabase_client()
    
    # Header
    st.markdown("<div class='header-title'>🗺️ Tesoros del Barrio</div>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"### 👤 {usuario['nombre']}")
        st.markdown(f"📧 {usuario['email']}")
        
        st.markdown("---")
        
        # Opciones del usuario
        opcion = st.radio(
            "🎯 Menú",
            ["🗺️ Mapa Interactivo", "➕ Agregar Lugar", "📋 Mis Lugares", "🔍 Explorar", "⚙️ Configuración"],
            key="menu_principal"
        )
        
        st.markdown("---")
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            AutenticacionManager.cerrar_sesion(client)
            st.session_state.autenticado = False
            st.session_state.usuario = None
            st.success("Sesión cerrada correctamente")
            st.rerun()
        
        st.markdown("---")
        st.markdown("**Tesoros del Barrio** v1.0  \n*Compartiendo lugares increíbles* 🌟")
    
    # Contenido principal según la opción seleccionada
    if opcion == "🗺️ Mapa Interactivo":
        pantalla_mapa(usuario, client)
    
    elif opcion == "➕ Agregar Lugar":
        pantalla_agregar_lugar(usuario, client)
    
    elif opcion == "📋 Mis Lugares":
        pantalla_mis_lugares(usuario, client)
    
    elif opcion == "🔍 Explorar":
        pantalla_explorar(usuario, client)
    
    elif opcion == "⚙️ Configuración":
        pantalla_configuracion(usuario, client)


def pantalla_mapa(usuario: Dict, client):
    """
    Muestra el mapa interactivo con todos los lugares.
    
    Args:
        usuario: Datos del usuario autenticado
        client: Cliente de Supabase
    """
    st.header("🗺️ Mapa Interactivo")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_categoria = st.selectbox(
            "Filtrar por categoría",
            ["Todas"] + LugaresManager.CATEGORIAS,
            key="filtro_categoria_mapa"
        )
    
    with col2:
        mostrar_solo_mios = st.checkbox("Solo mis lugares", key="solo_mios_mapa")
    
    with col3:
        auto_refresh = st.checkbox("Auto-actualizar", value=True, key="auto_refresh_mapa")
    
    # Obtener lugares
    if mostrar_solo_mios:
        lugares = LugaresManager.obtener_lugares_usuario(client, usuario["id"])
    elif filtro_categoria != "Todas":
        lugares = LugaresManager.obtener_lugares_por_categoria(client, filtro_categoria)
    else:
        lugares = LugaresManager.obtener_todos_lugares(client)
    
    if not lugares:
        st.info("📍 No hay lugares para mostrar. ¡Sé el primero en agregar uno!")
    else:
        # Mostrar estadísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de lugares", len(lugares))
        with col2:
            st.metric("Lugares por categoría", len(set(l["categoria"] for l in lugares)))
        with col3:
            st.metric("Contribuidores", len(set(l["autor_id"] for l in lugares)))
        
        st.markdown("---")
        
        # Crear y mostrar mapa
        try:
            mapa = crear_mapa(lugares)
            st_folium(mapa, width=1300, height=600)
        except Exception as e:
            st.error(f"Error al crear el mapa: {str(e)}")
        
        # Mostrar lista de lugares
        st.subheader("📌 Detalles de Lugares")
        for lugar in lugares:
            mostrar_card_lugar(lugar, usuario)


def pantalla_agregar_lugar(usuario: Dict, client):
    """
    Muestra el formulario para agregar un nuevo lugar.
    
    Args:
        usuario: Datos del usuario autenticado
        client: Cliente de Supabase
    """
    st.header("➕ Agregar Nuevo Lugar")
    
    st.markdown("""
    Comparte un lugar interesante de tu barrio. Completa todos los campos para crear un marcador en el mapa.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input(
            "Nombre del lugar",
            placeholder="Ej: Parque Central",
            help="Nombre corto y descriptivo"
        )
        
        categoria = st.selectbox(
            "Categoría",
            LugaresManager.CATEGORIAS,
            help="¿Qué tipo de lugar es?"
        )
        
        latitud = st.number_input(
            "Latitud",
            min_value=-90.0,
            max_value=90.0,
            value=4.7110,
            format="%.6f",
            help="Coordenada de latitud"
        )
    
    with col2:
        descripcion = st.text_area(
            "Descripción",
            placeholder="Describe el lugar en detalle",
            height=100,
            help="Información interesante sobre el lugar"
        )
        
        longitud = st.number_input(
            "Longitud",
            min_value=-180.0,
            max_value=180.0,
            value=-74.0055,
            format="%.6f",
            help="Coordenada de longitud"
        )
    
    # Sección de foto
    st.subheader("📸 Foto del Lugar (Opcional)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        foto_file = st.file_uploader(
            "Sube una foto",
            type=["jpg", "jpeg", "png", "gif", "webp"],
            help="Máximo 5 MB"
        )
    
    if foto_file is not None:
        with col2:
            image = Image.open(foto_file)
            st.image(image, caption="Vista previa", width=200)
    
    # Botón para crear
    st.markdown("---")
    
    if st.button("✅ Crear Lugar", use_container_width=True, type="primary"):
        # Validaciones
        if not nombre or not descripcion:
            st.error("Por favor completa nombre y descripción")
        else:
            try:
                # Subir foto si existe
                foto_url = None
                if foto_file is not None:
                    file_bytes = foto_file.read()
                    foto_url = SupabaseStorageManager.upload_photo(
                        client,
                        file_bytes,
                        foto_file.name,
                        usuario["id"]
                    )
                    
                    if foto_url is None:
                        st.warning("No se pudo subir la foto, pero se creará el lugar sin imagen")
                
                # Crear lugar
                success, message, lugar_id = LugaresManager.crear_lugar(
                    client,
                    nombre,
                    descripcion,
                    categoria,
                    latitud,
                    longitud,
                    usuario["id"],
                    foto_url
                )
                
                if success:
                    st.success(message)
                    st.balloons()
                    st.info(f"Lugar ID: {lugar_id}")
                else:
                    st.error(message)
            
            except Exception as e:
                st.error(f"Error al crear lugar: {str(e)}")


def pantalla_mis_lugares(usuario: Dict, client):
    """
    Muestra los lugares creados por el usuario autenticado.
    
    Args:
        usuario: Datos del usuario autenticado
        client: Cliente de Supabase
    """
    st.header("📋 Mis Lugares")
    
    lugares = LugaresManager.obtener_lugares_usuario(client, usuario["id"])
    
    if not lugares:
        st.info("🚫 Aún no has creado ningún lugar. ¡Comienza compartiendo uno!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Agregar mi primer lugar", use_container_width=True):
                st.switch_page("pages/main.py")
    else:
        st.markdown(f"Tienes **{len(lugares)}** lugares creados")
        st.markdown("---")
        
        # Mostrar opciones de filtro
        col1, col2 = st.columns(2)
        with col1:
            filtro_cat = st.selectbox("Filtrar por categoría", ["Todas"] + LugaresManager.CATEGORIAS)
        
        if filtro_cat != "Todas":
            lugares = [l for l in lugares if l["categoria"] == filtro_cat]
        
        # Mostrar lugares con opciones de edición
        for lugar in lugares:
            col1, col2 = st.columns([1, 0.15])
            
            with col1:
                with st.expander(f"{get_categoria_icon(lugar['categoria'])} {lugar['nombre']}", expanded=False):
                    st.markdown(f"**Descripción:** {lugar['descripcion']}")
                    st.markdown(f"**Categoría:** {lugar['categoria']}")
                    st.markdown(f"**Coordenadas:** ({lugar['latitud']:.4f}, {lugar['longitud']:.4f})")
                    st.markdown(f"**Creado:** {lugar['created_at'][:10]}")
                    
                    if lugar.get("foto_url"):
                        st.image(lugar["foto_url"], width=200)
            
            with col2:
                st.markdown("---")
                if st.button("✏️", key=f"edit_mis_{lugar['id']}", help="Editar"):
                    st.session_state.editar_lugar_id = lugar["id"]
                    st.rerun()
                
                if st.button("🗑️", key=f"delete_mis_{lugar['id']}", help="Eliminar"):
                    success, message = LugaresManager.eliminar_lugar(client, lugar["id"], usuario["id"])
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)


def pantalla_explorar(usuario: Dict, client):
    """
    Muestra una vista exploratoria de todos los lugares con filtros avanzados.
    
    Args:
        usuario: Datos del usuario autenticado
        client: Cliente de Supabase
    """
    st.header("🔍 Explorar Lugares")
    
    col1, col2 = st.columns(2)
    
    with col1:
        categoria_explorar = st.selectbox("Por categoría", ["Todas"] + LugaresManager.CATEGORIAS)
    
    with col2:
        orden_por = st.selectbox("Ordenar por", ["Más recientes", "Más antiguos"])
    
    # Obtener lugares con filtros
    if categoria_explorar == "Todas":
        lugares = LugaresManager.obtener_todos_lugares(client)
    else:
        lugares = LugaresManager.obtener_lugares_por_categoria(client, categoria_explorar)
    
    if orden_por == "Más antiguos":
        lugares = list(reversed(lugares))
    
    if not lugares:
        st.info("No hay lugares para mostrar")
    else:
        # Mostrar con columnas
        cols = st.columns(2)
        for idx, lugar in enumerate(lugares):
            with cols[idx % 2]:
                mostrar_card_lugar(lugar, usuario)
                
                # Mostrar imagen si existe
                if lugar.get("foto_url"):
                    try:
                        st.image(lugar["foto_url"], use_column_width=True)
                    except:
                        pass


def pantalla_configuracion(usuario: Dict, client):
    """
    Muestra opciones de configuración del usuario.
    
    Args:
        usuario: Datos del usuario autenticado
        client: Cliente de Supabase
    """
    st.header("⚙️ Configuración")
    
    st.subheader("👤 Información de Perfil")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Nombre:** {usuario['nombre']}")
    
    with col2:
        st.markdown(f"**Email:** {usuario['email']}")
    
    st.markdown("---")
    
    st.subheader("📊 Estadísticas")
    
    # Obtener estadísticas del usuario
    mis_lugares = LugaresManager.obtener_lugares_usuario(client, usuario["id"])
    todos_lugares = LugaresManager.obtener_todos_lugares(client)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Mis lugares", len(mis_lugares))
    
    with col2:
        st.metric("Total de lugares", len(todos_lugares))
    
    with col3:
        if mis_lugares:
            fecha_ultimo = mis_lugares[0]["created_at"][:10]
            st.metric("Último lugar", fecha_ultimo)
    
    st.markdown("---")
    
    st.subheader("🎨 Tema")
    
    tema = st.selectbox(
        "Selecciona el tema",
        ["Claro", "Oscuro", "Auto"],
        help="(Funcionalidad de ejemplo)"
    )
    
    st.markdown("---")
    
    st.subheader("ℹ️ Sobre la Aplicación")
    
    st.markdown("""
    **Tesoros del Barrio** v1.0
    
    Una aplicación colaborativa para descubrir y compartir lugares increíbles
    de tu vecindario con amigos y comunidad.
    
    **Características:**
    - 🗺️ Mapa interactivo con Folium
    - 👤 Autenticación segura con Supabase
    - 📸 Almacenamiento de fotos
    - 🔒 Row Level Security
    - 💬 Colaboración en tiempo real
    
    **Tecnologías:**
    - Python + Streamlit
    - Supabase (PostgreSQL + Auth)
    - Folium (mapas)
    
    Desarrollado con ❤️ por un desarrollador senior.
    """)


# ==========================================
# PUNTO DE ENTRADA PRINCIPAL
# ==========================================

def main():
    """
    Función principal de la aplicación.
    Controla el flujo entre autenticación y pantalla principal.
    """
    try:
        # Verificar conexión con Supabase
        if not verificar_conexion():
            st.error("""
            ❌ **Error de conexión con Supabase**
            
            ### Posibles soluciones:
            
            **Opción 1: En Streamlit Cloud**
            1. Abre tu app → Click en **⋮** (menú arriba a la derecha)
            2. Selecciona **"Manage app"**
            3. Ve a **Settings → Secrets**
            4. Verifica que existan estas variables (sin borrar ni modificar):
               ```
               SUPABASE_URL = "tu-url"
               SUPABASE_KEY = "tu-clave"
               ```
            5. Si no existen, agrégalas
            6. Haz click en **Save**
            7. Espera a que la app se redeploy automáticamente
            
            **Opción 2: Verifica que las credenciales sean correctas**
            - Ve a tu dashboard de Supabase
            - Copia la URL del proyecto (en Project Settings)
            - Copia la anon key (en Project Settings → API)
            - Asegúrate de usar la **anon key**, no la service role key
            
            **Opción 3: Reinicia la app**
            - En Streamlit Cloud, haz click en **⋮ → Reboot app**
            """)
            st.stop()
        
        # Inicializar session state
        inicializar_session_state()
        
        # Verificar autenticación
        usuario_actual = verificar_autenticacion()
        
        if usuario_actual and st.session_state.autenticado:
            # Usuario autenticado: mostrar pantalla principal
            pantalla_principal(usuario_actual)
        else:
            # No autenticado: mostrar pantalla de login/registro
            pantalla_autenticacion()
    
    except Exception as e:
        st.error(f"""
        ❌ Error inesperado: {str(e)}
        
        Por favor, recarga la página. Si el problema persiste, 
        contacta al administrador.
        """)
        print(f"Error en main(): {str(e)}")


if __name__ == "__main__":
    main()
