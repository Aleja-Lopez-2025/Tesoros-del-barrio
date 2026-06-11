# 🏗️ ARQUITECTURA DEL PROYECTO

Visión general técnica de Tesoros del Barrio.

---

## Diagrama de Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARIO FINAL                              │
│                    (Navegador Web)                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT (Frontend)                           │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  UI Components                                              │ │
│  │  - Sidebar                                                  │ │
│  │  - Forms                                                    │ │
│  │  - Maps (Folium)                                            │ │
│  │  - Cards/Dialogs                                            │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  app.py (~1,200 líneas)                                           │
│  - Pantalla de autenticación                                     │
│  - Pantalla principal                                             │
│  - Gestión de lugares                                             │
│  - Exploración                                                    │
│  - Configuración                                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                   LÓGICA DE NEGOCIO (Backend)                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Managers                                                   │ │
│  │                                                             │ │
│  │  AutenticacionManager          LugaresManager              │ │
│  │  ├─ registrar_usuario()        ├─ crear_lugar()           │ │
│  │  ├─ iniciar_sesion()           ├─ obtener_lugares()       │ │
│  │  ├─ obtener_usuario()          ├─ actualizar_lugar()      │ │
│  │  └─ cerrar_sesion()            ├─ eliminar_lugar()        │ │
│  │                                └─ filtrar_por_categoria() │ │
│  │                                                             │ │
│  │  utils/auth.py (280 líneas)    utils/places.py (400 líneas)│ │
│  └─────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│              CAPA DE ACCESO A DATOS (DAL)                        │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  SupabaseClient                                             │ │
│  │  - get_supabase_client()                                    │ │
│  │  - verificar_conexion()                                     │ │
│  │                                                             │ │
│  │  SupabaseStorageManager                                     │ │
│  │  - init_bucket()                                            │ │
│  │  - upload_photo()                                           │ │
│  │  - delete_photo()                                           │ │
│  │  - get_public_url()                                         │ │
│  │                                                             │ │
│  │  utils/supabase_client.py (250 líneas)                      │ │
│  └─────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                   SERVICIOS EXTERNOS (Cloud)                     │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  SUPABASE                                                   │ │
│  │  ┌──────────────────────────────────────────────────────┐   │ │
│  │  │  PostgreSQL Database                                │   │ │
│  │  │  • usuarios                                         │   │ │
│  │  │  • lugares                                          │   │ │
│  │  │  • logs_actividad                                   │   │ │
│  │  │  • Índices optimizados                              │   │ │
│  │  │  • Triggers de auditoría                            │   │ │
│  │  │  • Row Level Security (RLS)                         │   │ │
│  │  └──────────────────────────────────────────────────────┘   │ │
│  │  ┌──────────────────────────────────────────────────────┐   │ │
│  │  │  Authentication                                      │   │ │
│  │  │  • Email/Password Auth                              │   │ │
│  │  │  • JWT Tokens                                        │   │ │
│  │  │  • Session Management                               │   │ │
│  │  └──────────────────────────────────────────────────────┘   │ │
│  │  ┌──────────────────────────────────────────────────────┐   │ │
│  │  │  Storage                                              │   │ │
│  │  │  • Bucket: lugares-fotos                             │   │ │
│  │  │  • Fotos públicas                                    │   │ │
│  │  │  • CDN de imágenes                                   │   │ │
│  │  └──────────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Flujo de Datos

### Flujo de Registro

```
Usuario
    │
    ├─ Ingresa Email/Password/Nombre
    │
    ↓
app.py (pantalla_autenticacion)
    │
    ├─ Valida entrada
    │
    ↓
AutenticacionManager.registrar_usuario()
    │
    ├─ Crea usuario en auth (Supabase Auth)
    │ ├─ Hash de password
    │ └─ Genera UUID
    │
    ├─ Crea perfil en tabla usuarios
    │
    ↓
Supabase
    │
    ├─ auth.users (nuevo usuario)
    │
    ├─ public.usuarios (nuevo perfil)
    │
    ↓
Usuario → Mensaje de éxito → Puede iniciar sesión
```

### Flujo de Creación de Lugar

```
Usuario (autenticado)
    │
    ├─ Completa formulario
    │ ├─ Nombre
    │ ├─ Descripción
    │ ├─ Categoría
    │ ├─ Coordenadas
    │ └─ Foto (opcional)
    │
    ↓
app.py (pantalla_agregar_lugar)
    │
    ├─ Valida datos
    │
    ├─ Si hay foto:
    │ ├─ Valida tipo/tamaño
    │ │
    │ ↓ SupabaseStorageManager.upload_photo()
    │ │
    │ ├─ Sube a Storage
    │ ├─ Obtiene URL pública
    │
    ↓
LugaresManager.crear_lugar()
    │
    ├─ Valida coordenadas
    ├─ Verifica categoría válida
    │
    ↓
Supabase
    │
    ├─ Inserta en public.lugares
    │ ├─ RLS valida permisos
    │ ├─ Trigger actualiza timestamp
    │ └─ Índices optimizan búsqueda
    │
    ├─ Registra en logs_actividad
    │
    ↓
Usuario → Mensaje de éxito → Lugar aparece en mapa
         → Otros usuarios lo ven en tiempo real
```

### Flujo de Visualización en Mapa

```
Usuario abre "Mapa Interactivo"
    │
    ├─ Selecciona filtros:
    │ ├─ Categoría
    │ ├─ Solo mis lugares
    │ └─ Auto-refresh
    │
    ↓
app.py (pantalla_mapa)
    │
    ├─ Llama a LugaresManager
    │ ├─ obtener_todos_lugares()
    │ ├─ obtener_lugares_usuario()
    │ └─ obtener_lugares_por_categoria()
    │
    ↓
SupabaseClient
    │
    ├─ Query a public.lugares
    │ └─ JOIN con usuarios para autor info
    │
    ↓
Supabase
    │
    ├─ Aplica RLS (todos ven todos)
    ├─ Usa índices para rapidez
    ├─ Retorna con autor información
    │
    ↓
app.py
    │
    ├─ Crea mapa Folium
    │ ├─ Añade marcadores
    │ ├─ Asigna colores por categoría
    │ └─ Crea popups con info
    │
    ↓
Streamlit
    │
    ├─ Renderiza con st_folium()
    │
    ↓
Usuario
    │
    ├─ Ve mapa interactivo
    ├─ Puede hacer zoom/pan
    ├─ Puede hacer clic en marcadores
    └─ Ve popups con información
```

---

## Flujo de Autenticación

```
Session State (Streamlit)
    │
    ├─ autenticado: bool
    ├─ usuario: dict | None
    │
    ↓
verificar_autenticacion()
    │
    ├─ Verifica sesión activa
    ├─ Si no existe, intenta recuperar
    │
    ↓
AutenticacionManager.obtener_usuario_actual()
    │
    ├─ Consulta Supabase
    ├─ Obtiene usuario autenticado
    │
    ↓
Si usuario existe:
    ├─ Actualiza session_state
    ├─ Muestra app.py completa
Sino:
    └─ Muestra pantalla_autenticacion
```

---

## Estructura de Seguridad

```
┌─────────────────────────────────────────────────┐
│        APLICACIÓN (Streamlit)                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. Validación Frontend                          │
│     ├─ Email válido                             │
│     ├─ Password >= 6 caracteres                 │
│     ├─ Coordenadas válidas                      │
│     └─ Tamaño de archivo <= 5MB                 │
│                                                  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│        SUPABASE (Backend)                        │
├─────────────────────────────────────────────────┤
│                                                  │
│  2. Autenticación                                │
│     ├─ JWT Tokens                               │
│     ├─ Password Hashing (bcrypt)                │
│     └─ Session Management                       │
│                                                  │
│  3. Autorización (RLS)                          │
│     ├─ SELECT: Todos ven lugares                │
│     ├─ INSERT: Usuarios autenticados            │
│     ├─ UPDATE: Solo propietario                 │
│     └─ DELETE: Solo propietario                 │
│                                                  │
│  4. Integridad de Datos                         │
│     ├─ Constrains en tablas                     │
│     ├─ Índices para rapidez                     │
│     ├─ Triggers para auditoría                  │
│     └─ Foreign keys                             │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## Arquitectura de Modelos

### Modelo de Usuario

```
Usuario (Supabase Auth)
    │
    ├─ id: UUID
    ├─ email: string
    ├─ password: hash
    │
    ↓ (referencia)
    │
    Perfil (public.usuarios)
    ├─ id: UUID (FK → auth.users.id)
    ├─ nombre: string
    ├─ foto_perfil_url: string
    ├─ created_at: timestamp
    └─ updated_at: timestamp
```

### Modelo de Lugar

```
Lugar (public.lugares)
    │
    ├─ id: UUID
    ├─ nombre: string
    ├─ descripcion: text
    ├─ categoria: enum (6 opciones)
    ├─ latitud: decimal
    ├─ longitud: decimal
    ├─ foto_url: string (→ Storage)
    ├─ autor_id: UUID (FK → usuarios.id)
    ├─ created_at: timestamp
    └─ updated_at: timestamp
```

### Modelo de Log

```
Log (public.logs_actividad)
    │
    ├─ id: UUID
    ├─ usuario_id: UUID (FK)
    ├─ tipo_accion: string
    ├─ descripcion: text
    └─ created_at: timestamp
```

---

## Flujo de Despliegue

```
Desarrollo Local
    │
    ├─ Git repository
    ├─ .env con credenciales
    ├─ Python virtual environment
    └─ Streamlit dev server
    │
    ↓
GitHub Repository
    │
    ├─ Push a main branch
    ├─ All files committed
    │
    ↓
Deployment Platform (opciones)
    │
    ├─ Streamlit Cloud
    │ ├─ Detección automática
    │ ├─ Install requirements.txt
    │ ├─ Set environment secrets
    │ └─ Deploy automático
    │
    ├─ Heroku
    │ ├─ Procfile
    │ ├─ runtime.txt
    │ ├─ Git push heroku main
    │ └─ Config vars (secrets)
    │
    ├─ Docker
    │ ├─ docker build
    │ ├─ docker push (registry)
    │ └─ Ejecutar en cualquier platform
    │
    └─ Otros
        ├─ Railway
        ├─ Render
        ├─ Google Cloud Run
        └─ AWS ECS
    │
    ↓
Producción
    │
    ├─ HTTPS habilitado
    ├─ Supabase sincronizado
    ├─ Storage funcionando
    └─ Usuarios accediendo
```

---

## Stack Tecnológico Completo

```
FRONTEND
├─ Streamlit 1.38
├─ Folium 0.14
├─ Streamlit-Folium 0.19
└─ CSS Personalizado

BACKEND
├─ Python 3.11
├─ Supabase Client 2.3.5
└─ python-dotenv 1.0

DATOS
├─ PostgreSQL (via Supabase)
├─ Supabase Auth
└─ Supabase Storage

HERRAMIENTAS
├─ Docker
├─ Git
├─ pip (Python package manager)
└─ Streamlit CLI

DEPLOYMENT
├─ Streamlit Cloud
├─ Heroku
├─ Docker Registry
└─ Otros (Railway, Render, etc)
```

---

## Monitoreo y Observabilidad

```
Logs de Aplicación
    ↓
Streamlit (STDOUT)
    ↓
Platform logs (Heroku, Railway, etc)

Logs de Base de Datos
    ↓
public.logs_actividad
    ↓
Supabase Dashboard

Métricas
    ├─ Usuarios registrados
    ├─ Total de lugares
    ├─ Lugares por categoría
    ├─ Actividad por usuario
    └─ Uptime de la aplicación
```

---

## Decisiones Arquitectónicas

### 1. Modularidad
- ✅ Separación en utils/
- ✅ Managers para cada entidad
- ✅ Funciones reutilizables

### 2. Seguridad
- ✅ RLS en Supabase
- ✅ Validación en múltiples niveles
- ✅ Secrets en variables de entorno

### 3. Escalabilidad
- ✅ Índices en BD
- ✅ Caché de sesiones
- ✅ Storage separado

### 4. Mantenibilidad
- ✅ Código comentado
- ✅ Documentación completa
- ✅ Ejemplos de uso

### 5. Usabilidad
- ✅ Interfaz intuitiva
- ✅ Feedback inmediato
- ✅ Error handling

---

## Limitaciones y Consideraciones

### Actuales
- Testing: Manual (se puede automatizar)
- Real-time: Refreshes cada N segundos
- Caché: Session-based (se puede mejorar)

### Para el Futuro
- WebSocket para real-time puro
- Redis para caché global
- Tests automatizados (pytest)
- CI/CD pipeline

---

**Arquitectura:** Modular, escalable y segura  
**Complejidad:** Media (apropiada para el alcance)  
**Mantenibilidad:** Alta (bien documentada)  
**Rendimiento:** Bueno (optimizado)

¡La arquitectura está lista para producción! 🚀
