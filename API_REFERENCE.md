# 📖 Referencia de API - Guía de Desarrollo

Documentación técnica completa de los módulos de Tesoros del Barrio.

---

## 🔌 Módulo: `supabase_client.py`

Cliente y gestor de almacenamiento para Supabase.

### `get_supabase_client() -> Client`

Obtiene la instancia del cliente de Supabase.

```python
from utils.supabase_client import get_supabase_client

client = get_supabase_client()
# Ahora puedes usar client para operaciones en BD
```

**Retorna:**
- `Client`: Instancia de cliente Supabase conectada

**Excepciones:**
- `ValueError`: Si faltan variables de entorno

### `verificar_conexion() -> bool`

Verifica que la conexión con Supabase sea exitosa.

```python
from utils.supabase_client import verificar_conexion

if verificar_conexion():
    print("Conexión exitosa")
else:
    print("Error de conexión")
```

**Retorna:**
- `bool`: True si la conexión es válida

---

### Clase: `SupabaseStorageManager`

Gestiona operaciones con Supabase Storage.

#### Métodos Estáticos

##### `init_bucket(client: Client) -> bool`

Inicializa el bucket de almacenamiento.

```python
from utils.supabase_client import SupabaseStorageManager, get_supabase_client

client = get_supabase_client()
if SupabaseStorageManager.init_bucket(client):
    print("Bucket inicializado")
```

**Parámetros:**
- `client` (Client): Cliente Supabase

**Retorna:**
- `bool`: True si se inicializó correctamente

---

##### `upload_photo(client, file_bytes, file_name, usuario_id) -> str | None`

Sube una foto a Storage.

```python
from utils.supabase_client import SupabaseStorageManager

# Leer archivo
with open("foto.jpg", "rb") as f:
    file_bytes = f.read()

# Subir
url = SupabaseStorageManager.upload_photo(
    client,
    file_bytes,
    "foto.jpg",
    usuario_id="uuid-del-usuario"
)

if url:
    print(f"Foto subida: {url}")
else:
    print("Error al subir foto")
```

**Parámetros:**
- `client` (Client): Cliente Supabase
- `file_bytes` (bytes): Contenido del archivo
- `file_name` (str): Nombre del archivo
- `usuario_id` (str): ID del usuario

**Retorna:**
- `str`: URL pública del archivo
- `None`: Si hay error

**Validaciones:**
- Tamaño máximo: 5 MB
- Extensiones permitidas: .jpg, .jpeg, .png, .gif, .webp

---

##### `delete_photo(client, file_path) -> bool`

Elimina una foto del Storage.

```python
success = SupabaseStorageManager.delete_photo(client, "usuario-id/1234567_foto.jpg")
```

**Parámetros:**
- `client` (Client): Cliente Supabase
- `file_path` (str): Ruta del archivo

**Retorna:**
- `bool`: True si se eliminó correctamente

---

##### `get_public_url(file_path) -> str`

Obtiene la URL pública de un archivo.

```python
url = SupabaseStorageManager.get_public_url("usuario-id/1234567_foto.jpg")
```

**Parámetros:**
- `file_path` (str): Ruta del archivo

**Retorna:**
- `str`: URL pública del archivo

---

## 🔑 Módulo: `auth.py`

Gestión de autenticación de usuarios.

### Clase: `AutenticacionManager`

#### `registrar_usuario(email, password, nombre, client) -> (bool, str)`

Registra un nuevo usuario.

```python
from utils.auth import AutenticacionManager
from utils.supabase_client import get_supabase_client

client = get_supabase_client()

success, message = AutenticacionManager.registrar_usuario(
    email="usuario@example.com",
    password="MiPassword123",
    nombre="Juan Pérez",
    client=client
)

if success:
    print(message)  # "Registro exitoso..."
else:
    print(f"Error: {message}")
```

**Parámetros:**
- `email` (str): Email del usuario
- `password` (str): Contraseña (mín 6 caracteres)
- `nombre` (str): Nombre completo
- `client` (Client): Cliente Supabase

**Retorna:**
- `(bool, str)`: (éxito, mensaje)

**Posibles Errores:**
- Email ya registrado
- Contraseña muy corta
- Email inválido

---

#### `iniciar_sesion(email, password, client) -> (bool, str, dict | None)`

Inicia sesión de un usuario.

```python
success, message, usuario = AutenticacionManager.iniciar_sesion(
    email="usuario@example.com",
    password="MiPassword123",
    client=client
)

if success:
    print(f"Bienvenido {usuario['nombre']}")
    # usuario contiene: id, email, nombre, session
else:
    print(f"Error: {message}")
```

**Parámetros:**
- `email` (str): Email del usuario
- `password` (str): Contraseña
- `client` (Client): Cliente Supabase

**Retorna:**
- `(bool, str, dict|None)`: (éxito, mensaje, datos_usuario)

**Estructura de usuario:**
```python
{
    "id": "uuid",
    "email": "usuario@example.com",
    "nombre": "Juan Pérez",
    "session": {...}
}
```

---

#### `obtener_usuario_actual(client) -> dict | None`

Obtiene datos del usuario autenticado.

```python
usuario = AutenticacionManager.obtener_usuario_actual(client)

if usuario:
    print(f"Usuario: {usuario['nombre']}")
else:
    print("No hay sesión activa")
```

**Parámetros:**
- `client` (Client): Cliente Supabase

**Retorna:**
- `dict`: Datos del usuario
- `None`: Si no hay sesión

---

#### `cerrar_sesion(client) -> bool`

Cierra la sesión del usuario.

```python
if AutenticacionManager.cerrar_sesion(client):
    print("Sesión cerrada")
```

**Parámetros:**
- `client` (Client): Cliente Supabase

**Retorna:**
- `bool`: True si se cerró correctamente

---

### `inicializar_session_state()`

Inicializa el estado de Streamlit para autenticación.

```python
from utils.auth import inicializar_session_state

inicializar_session_state()

# Ahora puedes usar:
# st.session_state.autenticado
# st.session_state.usuario
```

---

### `verificar_autenticacion() -> dict | None`

Verifica si hay usuario autenticado y recupera sesión.

```python
from utils.auth import verificar_autenticacion

usuario_actual = verificar_autenticacion()

if usuario_actual:
    print(f"Bienvenido {usuario_actual['nombre']}")
else:
    print("Por favor, inicia sesión")
```

**Retorna:**
- `dict`: Datos del usuario autenticado
- `None`: Si no hay sesión

---

## 📍 Módulo: `places.py`

Gestión de lugares interesantes.

### Clase: `LugaresManager`

#### Constantes

```python
# Categorías disponibles
LugaresManager.CATEGORIAS = [
    "Parque",
    "Heladería",
    "Mural",
    "Mascotas",
    "Lugar secreto",
    "Otro"
]
```

#### `crear_lugar(cliente, nombre, descripcion, categoria, latitud, longitud, autor_id, foto_url) -> (bool, str, str|None)`

Crea un nuevo lugar.

```python
from utils.places import LugaresManager

success, message, lugar_id = LugaresManager.crear_lugar(
    cliente=client,
    nombre="Parque Central",
    descripcion="Parque bonito con árboles grandes",
    categoria="Parque",
    latitud=4.7110,
    longitud=-74.0055,
    autor_id="uuid-usuario",
    foto_url="https://storage.url/foto.jpg"  # opcional
)

if success:
    print(f"Lugar creado: {lugar_id}")
else:
    print(f"Error: {message}")
```

**Parámetros:**
- `cliente` (Client): Cliente Supabase
- `nombre` (str): Nombre del lugar
- `descripcion` (str): Descripción
- `categoria` (str): Una de las categorías disponibles
- `latitud` (float): -90 a 90
- `longitud` (float): -180 a 180
- `autor_id` (str): UUID del usuario
- `foto_url` (str, opcional): URL de la foto

**Retorna:**
- `(bool, str, str|None)`: (éxito, mensaje, lugar_id)

---

#### `obtener_lugar(cliente, lugar_id) -> dict | None`

Obtiene un lugar específico.

```python
lugar = LugaresManager.obtener_lugar(client, "uuid-lugar")

if lugar:
    print(f"Lugar: {lugar['nombre']}")
```

**Parámetros:**
- `cliente` (Client): Cliente Supabase
- `lugar_id` (str): UUID del lugar

**Retorna:**
- `dict`: Datos del lugar con autor
- `None`: Si no existe

---

#### `obtener_todos_lugares(cliente) -> list[dict]`

Obtiene todos los lugares.

```python
lugares = LugaresManager.obtener_todos_lugares(client)

for lugar in lugares:
    print(f"{lugar['nombre']} - {lugar['categoria']}")
```

**Parámetros:**
- `cliente` (Client): Cliente Supabase

**Retorna:**
- `list[dict]`: Lista de lugares

---

#### `obtener_lugares_usuario(cliente, usuario_id) -> list[dict]`

Obtiene lugares de un usuario específico.

```python
mis_lugares = LugaresManager.obtener_lugares_usuario(client, usuario_id)
```

**Parámetros:**
- `cliente` (Client): Cliente Supabase
- `usuario_id` (str): UUID del usuario

**Retorna:**
- `list[dict]`: Lugares del usuario

---

#### `obtener_lugares_por_categoria(cliente, categoria) -> list[dict]`

Obtiene lugares de una categoría.

```python
parques = LugaresManager.obtener_lugares_por_categoria(client, "Parque")
```

**Parámetros:**
- `cliente` (Client): Cliente Supabase
- `categoria` (str): Una de las categorías

**Retorna:**
- `list[dict]`: Lugares de la categoría

---

#### `actualizar_lugar(cliente, lugar_id, usuario_id, ...) -> (bool, str)`

Actualiza un lugar (solo propietario).

```python
success, message = LugaresManager.actualizar_lugar(
    cliente=client,
    lugar_id="uuid",
    usuario_id="uuid-usuario",
    nombre="Nuevo nombre",  # opcional
    descripcion="Nueva descripción",  # opcional
    categoria="Heladería"  # opcional
)
```

**Parámetros:**
- `cliente` (Client): Cliente Supabase
- `lugar_id` (str): UUID del lugar
- `usuario_id` (str): UUID del usuario
- Otros parámetros son opcionales

**Retorna:**
- `(bool, str)`: (éxito, mensaje)

**Validaciones:**
- El usuario debe ser el propietario
- Los datos deben ser válidos

---

#### `eliminar_lugar(cliente, lugar_id, usuario_id) -> (bool, str)`

Elimina un lugar (solo propietario).

```python
success, message = LugaresManager.eliminar_lugar(
    client,
    "uuid-lugar",
    "uuid-usuario"
)
```

**Parámetros:**
- `cliente` (Client): Cliente Supabase
- `lugar_id` (str): UUID del lugar
- `usuario_id` (str): UUID del usuario

**Retorna:**
- `(bool, str)`: (éxito, mensaje)

**Nota:**
- También elimina la foto asociada
- Solo el propietario puede eliminar

---

## 🎨 Funciones Auxiliares en `app.py`

### `get_categoria_color(categoria: str) -> str`

Retorna el color HEX de una categoría.

```python
color = get_categoria_color("Parque")  # "#90EE90"
```

**Retorna:**
- `str`: Color en formato hexadecimal

### `get_categoria_icon(categoria: str) -> str`

Retorna emoji de una categoría.

```python
icon = get_categoria_icon("Heladería")  # "🍦"
```

**Retorna:**
- `str`: Emoji representativo

### `crear_mapa(lugares: list, centro_lat: float, centro_lon: float) -> folium.Map`

Crea mapa interactivo de Folium.

```python
from app import crear_mapa

mapa = crear_mapa(lugares, 4.7110, -74.0055)
# mapa es un objeto folium.Map listo para st_folium()
```

**Parámetros:**
- `lugares` (list): Lista de lugares
- `centro_lat` (float): Latitud del centro (default: Bogotá)
- `centro_lon` (float): Longitud del centro (default: Bogotá)

**Retorna:**
- `folium.Map`: Mapa interactivo

---

## 💡 Ejemplos de Uso Completos

### Ejemplo 1: Crear lugar y subirlo con foto

```python
from utils.supabase_client import get_supabase_client, SupabaseStorageManager
from utils.places import LugaresManager

# 1. Obtener cliente
client = get_supabase_client()

# 2. Subir foto
with open("foto.jpg", "rb") as f:
    file_bytes = f.read()

foto_url = SupabaseStorageManager.upload_photo(
    client,
    file_bytes,
    "foto.jpg",
    usuario_id="uuid"
)

# 3. Crear lugar con foto
if foto_url:
    success, msg, lugar_id = LugaresManager.crear_lugar(
        client,
        "Mi Lugar",
        "Descripción",
        "Parque",
        4.7110,
        -74.0055,
        "uuid",
        foto_url
    )
```

### Ejemplo 2: Listar y filtrar lugares

```python
# Obtener todos los lugares
todos = LugaresManager.obtener_todos_lugares(client)

# Filtrar por categoría
parques = [l for l in todos if l['categoria'] == 'Parque']

# Filtrar por usuario
mis_lugares = LugaresManager.obtener_lugares_usuario(client, "uuid")
```

### Ejemplo 3: Flujo de autenticación

```python
from utils.auth import AutenticacionManager, verificar_autenticacion

# Registrar
ok, msg = AutenticacionManager.registrar_usuario(...)

# Iniciar sesión
ok, msg, user = AutenticacionManager.iniciar_sesion(...)

# Verificar sesión activa
usuario = verificar_autenticacion()
```

---

## 🔧 Configuración de Variables de Entorno

```env
# .env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
DEBUG=false
MAPBOX_TOKEN=sk_live_...  # Opcional
```

---

## ⚠️ Manejo de Errores

Todos los métodos incluyen manejo de errores:

```python
try:
    success, message = LugaresManager.crear_lugar(...)
    if not success:
        print(f"Error: {message}")
except Exception as e:
    print(f"Error inesperado: {e}")
```

---

## 🧪 Testing Manual

```python
# test_api.py
from utils.supabase_client import get_supabase_client, verificar_conexion
from utils.auth import AutenticacionManager
from utils.places import LugaresManager

# Verificar conexión
print("Verificando conexión...", verificar_conexion())

# Obtener cliente
client = get_supabase_client()

# Listar lugares
lugares = LugaresManager.obtener_todos_lugares(client)
print(f"Total de lugares: {len(lugares)}")

# Verificar usuario
usuario = AutenticacionManager.obtener_usuario_actual(client)
print(f"Usuario autenticado: {usuario is not None}")
```

---

## 📊 Tipos de Datos

### Estructura de Usuario

```python
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "foto_perfil_url": "https://...",
    "created_at": "2024-01-15T10:30:00+00:00",
    "updated_at": "2024-01-15T10:30:00+00:00"
}
```

### Estructura de Lugar

```python
{
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "nombre": "Parque Central",
    "descripcion": "Un hermoso parque...",
    "categoria": "Parque",
    "latitud": 4.7110,
    "longitud": -74.0055,
    "foto_url": "https://storage.url/foto.jpg",
    "autor_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-01-15T10:30:00+00:00",
    "updated_at": "2024-01-15T10:30:00+00:00",
    "usuarios": {
        "nombre": "Juan Pérez",
        "email": "juan@example.com"
    }
}
```

---

## 📞 Soporte

Si necesitas ayuda con la API:

1. Revisa los comentarios del código
2. Lee los ejemplos en este documento
3. Abre un Issue en GitHub
4. Consulta la documentación oficial

---

**Versión:** 1.0.0  
**Última actualización:** 2024
