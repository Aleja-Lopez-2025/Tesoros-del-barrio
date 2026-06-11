# Tesoros del Barrio - Guía de Instalación y Despliegue

## 📋 Descripción General

**Tesoros del Barrio** es una aplicación web colaborativa que permite a niños y amigos descubrir y compartir lugares interesantes de su vecindario mediante un mapa interactivo.

### Características Principales

✅ **Autenticación segura** - Registro y login de usuarios  
✅ **Mapa interactivo** - Visualización en tiempo real con Folium  
✅ **Gestión de lugares** - Crear, editar y eliminar lugares  
✅ **Almacenamiento de fotos** - Imágenes en Supabase Storage  
✅ **Row Level Security** - Protección de datos  
✅ **Interfaz moderna** - Diseño responsive y amigable  

---

## 🚀 Instalación Local

### 1. Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Una cuenta en [Supabase](https://supabase.com) (gratuita)
- Git (opcional)

### 2. Clonar el Repositorio

```bash
cd tu-carpeta-de-proyectos
git clone https://github.com/tu-usuario/tesoros-del-barrio.git
cd tesoros-del-barrio
```

### 3. Crear un Entorno Virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

1. Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

2. Edita `.env` y completa con tus credenciales de Supabase:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key-aqui
DEBUG=false
```

### 6. Configurar Supabase

#### a) Crear el Proyecto en Supabase

1. Ve a [supabase.com](https://supabase.com) y crea una cuenta
2. Crea un nuevo proyecto
3. Copia la URL y la anon key a tu archivo `.env`

#### b) Crear las Tablas

1. Ve al SQL Editor en Supabase
2. Copia el contenido de `sql/setup.sql`
3. Ejecuta las sentencias SQL
4. Luego copia y ejecuta el contenido de `sql/rls.sql`

#### c) Crear el Bucket de Storage

1. Ve a Storage en el panel de Supabase
2. Crea un nuevo bucket llamado `lugares-fotos`
3. Configúralo como público

### 7. Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

---

## 📁 Estructura del Proyecto

```
tesoros-del-barrio/
├── app.py                      # Aplicación principal de Streamlit
├── requirements.txt            # Dependencias de Python
├── .env.example               # Variables de entorno (plantilla)
├── .streamlit/
│   └── config.toml           # Configuración de Streamlit
├── utils/
│   ├── __init__.py           # Inicializador del paquete
│   ├── supabase_client.py    # Cliente y storage de Supabase
│   ├── auth.py               # Gestión de autenticación
│   └── places.py             # Gestión de lugares
└── sql/
    ├── setup.sql             # Creación de tablas y triggers
    └── rls.sql               # Políticas de Row Level Security
```

---

## 🗄️ Estructura de la Base de Datos

### Tabla `usuarios`

```sql
- id (UUID, PK)
- nombre (VARCHAR)
- email (VARCHAR, UNIQUE)
- foto_perfil_url (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### Tabla `lugares`

```sql
- id (UUID, PK)
- nombre (VARCHAR)
- descripcion (TEXT)
- categoria (VARCHAR) - Parque, Heladería, Mural, Mascotas, Lugar secreto, Otro
- latitud (DECIMAL)
- longitud (DECIMAL)
- foto_url (TEXT)
- autor_id (UUID, FK → usuarios.id)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### Tabla `logs_actividad`

```sql
- id (UUID, PK)
- usuario_id (UUID, FK → usuarios.id)
- tipo_accion (VARCHAR)
- descripcion (TEXT)
- created_at (TIMESTAMP)
```

---

## 🔒 Seguridad

La aplicación implementa **Row Level Security (RLS)** en Supabase:

### Políticas de Seguridad

- ✅ Los usuarios pueden ver todos los lugares
- ✅ Los usuarios pueden crear lugares (solo sus propios lugares)
- ✅ Los usuarios solo pueden editar sus propios lugares
- ✅ Los usuarios solo pueden eliminar sus propios lugares
- ✅ Las contraseñas se almacenan de forma segura con Supabase Auth

---

## 🌐 Despliegue en Producción

### Opción 1: Streamlit Cloud (Recomendado)

1. Sube tu proyecto a GitHub
2. Ve a [streamlit.io/cloud](https://streamlit.io/cloud)
3. Conecta tu repositorio
4. Configura las variables de entorno en la plataforma
5. ¡Listo! Tu app estará en línea

### Opción 2: Heroku

1. Instala Heroku CLI
2. Crea un archivo `Procfile`:

```
web: streamlit run app.py --logger.level=error
```

3. Crea un archivo `runtime.txt`:

```
python-3.11.0
```

4. Despliega:

```bash
heroku create tu-app-tesoros
git push heroku main
```

### Opción 3: Docker

Crea un `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--logger.level=error"]
```

Construye y ejecuta:

```bash
docker build -t tesoros-del-barrio .
docker run -p 8501:8501 -e SUPABASE_URL=... -e SUPABASE_KEY=... tesoros-del-barrio
```

---

## 🔧 Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| SUPABASE_URL | URL de tu proyecto Supabase | https://xxxxx.supabase.co |
| SUPABASE_KEY | Anon key de Supabase | eyJhbG... |
| DEBUG | Modo debug (false/true) | false |

---

## 📝 Uso de la Aplicación

### Para Usuarios

1. **Registrarse** - Crea una cuenta con tu email
2. **Iniciar sesión** - Accede con tus credenciales
3. **Explorar mapa** - Ve todos los lugares en el mapa
4. **Agregar lugar** - Comparte un nuevo lugar con foto
5. **Editar/Eliminar** - Gestiona tus propios lugares

### Categorías de Lugares

- 🌳 **Parque** - Áreas verdes, parques públicos
- 🍦 **Heladería** - Tiendas de helado
- 🎨 **Mural** - Arte urbano y murales
- 🐾 **Mascotas** - Lugares amigables con mascotas
- 🔐 **Lugar secreto** - Lugares especiales y ocultos
- 📍 **Otro** - Cualquier otro lugar interesante

---

## 🐛 Solución de Problemas

### Error: "Variables de entorno no encontradas"

**Solución:** Asegúrate de tener un archivo `.env` en la raíz del proyecto con:
```env
SUPABASE_URL=tu-url
SUPABASE_KEY=tu-key
```

### Error: "No se puede conectar a Supabase"

**Solución:** Verifica que:
- ✅ Las credenciales sean correctas
- ✅ El proyecto de Supabase esté activo
- ✅ Tengas conexión a Internet

### Imágenes no se cargan

**Solución:** 
- Verifica que el bucket `lugares-fotos` existe en Storage
- Asegúrate que está configurado como público
- Comprueba que el archivo se subió correctamente

### Error de permisos al editar/eliminar lugares

**Solución:** Revisa que el RLS está correctamente configurado:
```bash
# En Supabase SQL Editor, ejecuta:
SELECT * FROM pg_policies;
```

---

## 📊 Monitoreo y Análisis

### Logs de Actividad

Todos los eventos se registran en la tabla `logs_actividad`:

```sql
SELECT * FROM logs_actividad ORDER BY created_at DESC LIMIT 10;
```

### Estadísticas de Lugares

```sql
SELECT categoria, COUNT(*) as total 
FROM lugares 
GROUP BY categoria 
ORDER BY total DESC;
```

---

## 🤝 Contribuciones

¿Quieres mejorar Tesoros del Barrio? ¡Bienvenido!

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-feature`)
3. Commit tus cambios (`git commit -m 'Agrega nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 📧 Soporte

¿Tienes problemas o sugerencias? Contacta a:

- 📧 Email: soporte@tesorosdelbarrio.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

## 🙏 Agradecimientos

- ❤️ Streamlit por el framework web increíble
- 🚀 Supabase por la base de datos y autenticación
- 🗺️ Folium por los mapas interactivos
- 👨‍💻 Comunidad de desarrolladores Python

---

**Versión:** 1.0.0  
**Última actualización:** 2024  
**Estado:** ✅ Producción

¡Disfruta compartiendo los tesoros de tu barrio! 🌟🗺️
