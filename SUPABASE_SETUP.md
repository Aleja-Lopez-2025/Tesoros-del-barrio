# Guía Rápida de Supabase

## 🚀 Pasos para Configurar Supabase

### 1. Crear Proyecto en Supabase

1. Ve a https://supabase.com
2. Haz clic en "Start your project"
3. Inicia sesión o crea una cuenta
4. Crea un nuevo proyecto:
   - Nombre: `tesoros-del-barrio`
   - Contraseña de BD: Genera una segura
   - Región: Elige la más cercana a ti
5. Espera a que se cree el proyecto (puede tomar 2-3 minutos)

### 2. Obtener Credenciales

1. Ve a **Settings** → **API**
2. Busca:
   - **Project URL** → Copia esto a `SUPABASE_URL` en `.env`
   - **anon public** → Copia esto a `SUPABASE_KEY` en `.env`

### 3. Ejecutar SQL Setup

1. Ve a **SQL Editor** en el panel lateral
2. Haz clic en "+ New Query"
3. Copia TODO el contenido de `sql/setup.sql`
4. Pega en el editor
5. Haz clic en "Run" (ícono de play)
6. Espera a que se ejecute

### 4. Ejecutar SQL RLS

1. Nuevamente en **SQL Editor** → "+ New Query"
2. Copia TODO el contenido de `sql/rls.sql`
3. Pega en el editor
4. Haz clic en "Run"
5. Espera a que se ejecute

### 5. Crear Bucket de Storage

1. Ve a **Storage** en el panel lateral
2. Haz clic en "Create a new bucket"
3. Nombre: `lugares-fotos`
4. ✅ Habilita "Public bucket"
5. Haz clic en "Create bucket"

### 6. Verificar Autenticación

1. Ve a **Authentication** → **Providers**
2. Verifica que "Email" esté habilitado (debería estarlo por defecto)

### 7. Archivos de Configuración en Supabase

Supabase debería tener automáticamente configurado:
- ✅ Autenticación por email/contraseña
- ✅ RLS habilitado
- ✅ Funciones y triggers (del setup.sql)

---

## 🧪 Probar la Configuración

### Desde Supabase Console

1. Ve a **Table Editor**
2. Verifica que existan las tablas:
   - `usuarios`
   - `lugares`
   - `logs_actividad`

### Desde la Aplicación

1. Instala dependencias: `pip install -r requirements.txt`
2. Crea `.env` con tus credenciales
3. Ejecuta: `streamlit run app.py`
4. En el navegador, ve a `http://localhost:8501`
5. Intenta registrarte y crear un lugar

---

## 🔑 Gestión de Credenciales

### Variables de Entorno Necesarias

```bash
# .env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**⚠️ IMPORTANTE:** 
- Nunca compartas tu `SUPABASE_KEY` en público
- No subas `.env` a GitHub
- Para producción, usa variables de entorno del servidor

---

## 📊 Monitoreo en Supabase

### Ver Usuarios Registrados

En **Authentication** → **Users**, verás todos los usuarios registrados.

### Ver Lugares Creados

En **Table Editor** → **lugares**, verás todos los lugares.

### Monitorear Logs de Actividad

En **Table Editor** → **logs_actividad**, verás todas las acciones.

### Ver Storage Files

En **Storage** → **lugares-fotos**, verás todas las imágenes subidas.

---

## 🔐 Seguridad Recomendada

### Para Desarrollo
- Usa credenciales de Supabase en `.env`
- No compartas el archivo `.env`

### Para Producción
1. Crea una aplicación de Supabase separada para producción
2. Usa variables de entorno del servidor (Streamlit Cloud, Heroku, etc.)
3. Rota las claves regularmente
4. Habilita 2FA en tu cuenta de Supabase
5. Revisa los logs de acceso en Supabase

---

## 🆘 Problemas Comunes

### Error: "Invalid API Key"

**Solución:** Copia la **anon key**, no la **service_role key**

### Error: "Project not found"

**Solución:** Asegúrate que el `SUPABASE_URL` sea completo (incluye `/`)

### Las tablas no se crean

**Solución:** 
1. Verifica los errores en el SQL Editor
2. Copia el contenido de `setup.sql` línea por línea
3. Intenta nuevamente

### El bucket no se crea

**Solución:** 
1. Ve a Storage
2. Haz clic en "New bucket"
3. Asegúrate de habilitar "Public bucket"
4. Los archivos deben ser públicos para mostrar imágenes

---

## 📱 Conectar desde la App

```python
from utils.supabase_client import get_supabase_client

client = get_supabase_client()
# Ahora puedes usar: client.table("lugares").select("*").execute()
```

---

## 🚀 Desplegar a Producción

### En Streamlit Cloud

1. Sube tu código a GitHub
2. Ve a https://share.streamlit.io
3. Conecta tu repositorio
4. En **Advanced Settings**, agrega:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
5. ¡Listo! Tu app está en línea

### En Heroku

1. Sigue las instrucciones en el README.md
2. Configura las variables de entorno con:
   ```bash
   heroku config:set SUPABASE_URL=...
   heroku config:set SUPABASE_KEY=...
   ```

---

## 📞 Recursos

- 📚 [Documentación Supabase](https://supabase.com/docs)
- 🎓 [Tutoriales Supabase](https://supabase.com/learn)
- 🛠️ [Dashboard Supabase](https://app.supabase.com)
- 💬 [Comunidad Supabase](https://discord.supabase.com)

---

¡Listo! Tu Supabase está configurado. ¡Ahora ejecuta `streamlit run app.py`! 🚀
