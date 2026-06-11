# Guía de Despliegue en Producción

## 🚀 Opciones de Despliegue

Tesoros del Barrio se puede desplegar en varios servicios en la nube. Aquí están las opciones más populares:

---

## 1️⃣ **Streamlit Cloud** (Recomendado - Gratuito)

### Ventajas
✅ Gratuito  
✅ Integración directa con GitHub  
✅ Dominio gratuito  
✅ Automático con cada push  
✅ Manejo de secretos  

### Pasos

#### Paso 1: Preparar el Repositorio

```bash
# Asegúrate que tu proyecto esté en GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/tesoros-del-barrio.git
git push -u origin main
```

#### Paso 2: Conectar con Streamlit Cloud

1. Ve a https://share.streamlit.io
2. Haz clic en "Deploy an app"
3. Pega la URL de tu repositorio GitHub
4. Selecciona la rama: `main`
5. Ruta del archivo: `app.py`
6. Haz clic en "Deploy"

#### Paso 3: Configurar Secretos

1. Una vez desplegada, ve a "Advanced settings"
2. En la sección de secretos, agrega:

```toml
[secrets]
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_KEY = "tu-anon-key-aqui"
```

3. Guarda y la app se recargará

#### Paso 4: Actualizar `.env.example`

En tu código, puedes acceder a los secretos así:

```python
import streamlit as st

supabase_url = st.secrets.get("SUPABASE_URL")
supabase_key = st.secrets.get("SUPABASE_KEY")
```

Pero ya está implementado en `utils/supabase_client.py`, así que solo configurando los secretos funcionará.

---

## 2️⃣ **Heroku** (Gratuito con limitaciones)

### Ventajas
✅ Flexible  
✅ Control total  
✅ Múltiples apps  
✅ Variables de entorno fáciles  

### Requisitos
- Cuenta en Heroku
- Heroku CLI instalado
- Tarjeta de crédito (verificación)

### Pasos

#### Paso 1: Instalar Heroku CLI

```bash
# Windows
choco install heroku-cli

# macOS
brew install heroku/brew/heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### Paso 2: Crear Archivos de Configuración

Crea `Procfile` en la raíz:

```
web: streamlit run app.py --logger.level=error --server.port=$PORT
```

Crea `runtime.txt`:

```
python-3.11.1
```

Crea `.gitignore`:

```
venv/
.env
__pycache__/
*.pyc
.DS_Store
```

#### Paso 3: Desplegar

```bash
# Login en Heroku
heroku login

# Crear app
heroku create tu-app-tesoros-del-barrio

# Configurar variables de entorno
heroku config:set SUPABASE_URL=https://tu-proyecto.supabase.co
heroku config:set SUPABASE_KEY=tu-anon-key-aqui

# Desplegar
git push heroku main

# Ver logs
heroku logs --tail
```

#### Paso 4: Acceder

```
https://tu-app-tesoros-del-barrio.herokuapp.com
```

---

## 3️⃣ **Docker + Railway/Render** (Recomendado para escala)

### Ventajas
✅ Contenedor completo  
✅ Escalable  
✅ Control total  
✅ Múltiples regiones  

### Crear Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8501

# Configurar Streamlit
RUN mkdir -p ~/.streamlit && \
    echo "[server]" > ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "enableXsrfProtection = false" >> ~/.streamlit/config.toml

# Ejecutar
CMD ["streamlit", "run", "app.py"]
```

### Desplegar en Railway

```bash
# Instalar CLI de Railway
npm i -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Agregar archivo railroad.toml en la raíz
cat > railroad.toml << EOF
[build]
builder = "dockerfile"

[deploy]
healthcheckPath = "/"
EOF

# Desplegar
railway up

# Configurar variables de entorno en dashboard
# SUPABASE_URL=...
# SUPABASE_KEY=...

# Ver URL pública
railway status
```

### Desplegar en Render

1. Ve a https://render.com
2. Conecta tu GitHub
3. Create New → Web Service
4. Selecciona tu repositorio
5. Selecciona Dockerfile
6. Agrega las variables de entorno:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
7. Deploy

---

## 4️⃣ **Google Cloud Run** (Gratuito con límites)

### Ventajas
✅ Escalable automáticamente  
✅ Paga solo lo que uses  
✅ Integración con Google Cloud  

### Pasos

```bash
# 1. Instalar Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# 2. Autenticarse
gcloud auth login

# 3. Configurar proyecto
gcloud config set project tu-proyecto-id

# 4. Crear archivo .dockerignore
echo "venv
.git
.env
__pycache__" > .dockerignore

# 5. Desplegar
gcloud run deploy tesoros-del-barrio \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --allow-unauthenticated \
  --set-env-vars SUPABASE_URL=https://tu-proyecto.supabase.co,SUPABASE_KEY=tu-key

# 6. Ver URL
gcloud run services list
```

---

## 5️⃣ **AWS Elastic Beanstalk**

### Pasos

```bash
# 1. Instalar EB CLI
pip install awsebcli

# 2. Inicializar
eb init -p python-3.11 tesoros-del-barrio --region us-east-1

# 3. Crear entorno
eb create tesoros-del-barrio-env

# 4. Configurar variables de entorno
eb setenv SUPABASE_URL=... SUPABASE_KEY=...

# 5. Desplegar
eb deploy

# 6. Ver estado
eb status
```

---

## 🔄 Actualizar la App en Producción

### En Streamlit Cloud

```bash
# Solo haz push a GitHub, se actualiza automáticamente
git add .
git commit -m "Update app"
git push origin main
```

### En Heroku

```bash
git add .
git commit -m "Update app"
git push heroku main
```

### En Docker/Railway/Render

```bash
git add .
git commit -m "Update app"
git push origin main
# Se actualiza automáticamente con GitHub

# O manualmente
railway up  # Para Railway
# O pushear a Render manualmente desde dashboard
```

---

## 📊 Monitoreo en Producción

### Streamlit Cloud

- Ve al dashboard
- Haz clic en tu app
- Ve la pestaña "Logs"

### Heroku

```bash
heroku logs --tail
```

### Railway/Render

- Ve al dashboard
- Haz clic en Deployments
- Ve los logs

---

## 🔒 Seguridad en Producción

### Checklist de Seguridad

- ✅ `.env` nunca en Git (usa `.gitignore`)
- ✅ Credenciales en variables de entorno del servidor
- ✅ HTTPS habilitado (automático en la mayoría de plataformas)
- ✅ RLS configurado en Supabase
- ✅ Backups automáticos en Supabase
- ✅ CORS configurado si es necesario

### Habilitar Backups en Supabase

1. Ve a **Settings** → **Backups**
2. Habilita "Point in time recovery"
3. Elige retención de backups

---

## 💰 Costos Estimados (Mensual)

| Servicio | Gratis | Pago |
|----------|--------|------|
| Streamlit Cloud | ✅ | No aplicable |
| Heroku | ✅* | $5+ |
| Railway | 5 USD | Por uso |
| Render | ✅* | Por uso |
| Google Cloud Run | 2M requests | $0.40/M |
| AWS Beanstalk | 750h/mes* | Por uso |
| Supabase | 500 MB | $25+ |

*Con limitaciones

---

## 🚨 Solución de Problemas

### Error: "Memory exceeded"

**Solución:**
- Reduce el tamaño de imágenes antes de subir
- Usa compresión en el Storage

### Error: "Timeout"

**Solución:**
- Aumenta el timeout en la configuración
- Optimiza las consultas a BD

### Error: "Port already in use"

**Solución:**
- El puerto 8501 ya está en uso
- En Docker: expone un puerto diferente

### Error: "CORS policy"

**Solución:**
- Configura CORS en Supabase
- En **Settings** → **API**, agrega tu dominio

---

## 📈 Escalabilidad

### Para muchos usuarios:

1. **Supabase**
   - Usa un plan pagado
   - Habilita read-only replicas
   - Optimiza índices de base de datos

2. **Streamlit Cloud**
   - Usa la opción "Scale"
   - Considera un servicio de caché (Redis)

3. **Docker**
   - Escala horizontalmente
   - Usa Kubernetes (K8s)

---

## 📞 Ayuda y Recursos

- 📚 [Streamlit Docs](https://docs.streamlit.io)
- 🚀 [Deploy Streamlit](https://docs.streamlit.io/streamlit-cloud/get-started)
- 🐳 [Docker Guide](https://docs.docker.com)
- 🚂 [Railway Docs](https://docs.railway.app)
- 🎨 [Render Docs](https://docs.render.com)

---

**¡Tu Tesoros del Barrio está listo para producción! 🎉**
