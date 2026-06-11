# 🚀 Quick Start - Inicio Rápido

Comienza con Tesoros del Barrio en **menos de 5 minutos**.

## 📦 Instalación Rápida

### 1. Descargar el Proyecto

```bash
git clone https://github.com/tu-usuario/tesoros-del-barrio.git
cd tesoros-del-barrio
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Supabase (⏱️ 2 minutos)

#### Opción A: Crear Proyecto Nuevo (Recomendado)

1. Ve a https://supabase.com/dashboard
2. Haz clic en **"New project"**
3. Completa:
   - **Name:** `tesoros-del-barrio`
   - **Password:** Una contraseña fuerte (guarda esta contraseña)
   - **Region:** La más cercana a ti
4. Espera 2-3 minutos

#### Opción B: Usar Proyecto Existente

Si ya tienes un proyecto, solo copia las credenciales.

### 5. Copiar Credenciales

1. Ve a **Settings → API**
2. Copia:
   ```
   Project URL (SUPABASE_URL)
   anon public key (SUPABASE_KEY)
   ```

3. Crea archivo `.env`:
   ```bash
   cp .env.example .env
   ```

4. Edita `.env` y pega las credenciales:
   ```env
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJhbGci...
   ```

### 6. Configurar Base de Datos (⏱️ 2 minutos)

1. En Supabase, ve a **SQL Editor**
2. Copia TODO el contenido de `sql/setup.sql`
3. Pega en el editor de SQL
4. Haz clic en **Run**
5. Repite con `sql/rls.sql`

### 7. Crear Storage Bucket

1. Ve a **Storage** en Supabase
2. Haz clic en **"Create a new bucket"**
3. Nombre: `lugares-fotos`
4. ✅ Marca: "Public bucket"
5. Haz clic en **"Create bucket"**

### 8. ¡Ejecutar la App!

```bash
streamlit run app.py
```

Se abrirá en `http://localhost:8501`

---

## 🎮 Primeros Pasos en la App

### Registrarse

1. Ve a la pestaña "Registro"
2. Completa:
   - Nombre: Tu nombre
   - Email: tu@email.com
   - Contraseña: Mínimo 6 caracteres
3. Haz clic en **"Registrarse"**

### Agregar tu Primer Lugar

1. En el menú, haz clic en **"➕ Agregar Lugar"**
2. Completa:
   - **Nombre:** Ej: "Parque Central"
   - **Descripción:** Describe el lugar
   - **Categoría:** Elige una
   - **Latitud/Longitud:** (Usa coordenadas de tu barrio)
   - **Foto:** (Opcional) Sube una imagen
3. Haz clic en **"✅ Crear Lugar"**

### Ver en el Mapa

1. Ve a **"🗺️ Mapa Interactivo"**
2. Verás todos los lugares en el mapa
3. Haz clic en un marcador para ver detalles

---

## 📍 Coordenadas Rápidas

Si no sabes las coordenadas de tu lugar:

1. Ve a Google Maps
2. Haz clic derecho en el lugar
3. Se mostrarán las coordenadas
4. Copia latitud y longitud

### Ciudades Principales

| Ciudad | Latitud | Longitud |
|--------|---------|----------|
| Bogotá | 4.7110 | -74.0055 |
| Medellín | 6.2442 | -75.5812 |
| Cali | 3.4372 | -76.5069 |
| Barranquilla | 10.9639 | -74.7964 |
| Cartagena | 10.3806 | -75.5152 |

---

## 🆘 Problemas Comunes

### "Variables de entorno no encontradas"

```bash
# Asegúrate de tener .env en la raíz del proyecto
ls .env

# Si no existe:
cp .env.example .env
# Luego edita .env con tus credenciales
```

### "No se puede conectar a Supabase"

- Verifica las credenciales en `.env`
- Verifica que el proyecto esté activo en Supabase
- Recarga la página

### "Las imágenes no se cargan"

- Verifica que el bucket `lugares-fotos` existe
- Verifica que está marcado como público
- Intenta subir la imagen de nuevo

### "Error al crear lugar"

- Asegúrate que las coordenadas sean válidas
- Latitud: -90 a 90
- Longitud: -180 a 180

---

## ✅ Checklist de Instalación

- [ ] Proyecto clonado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Proyecto Supabase creado
- [ ] `.env` configurado
- [ ] SQL ejecutado
- [ ] Bucket creado
- [ ] App ejecutada
- [ ] Registro completado
- [ ] Primer lugar creado

---

## 🎯 Próximos Pasos

### Explorar la App

1. Crea varios lugares
2. Prueba los filtros
3. Intenta editar y eliminar lugares
4. Explora todas las secciones

### Personalizar

- Cambia colores en `app.py`
- Modifica el CSS en la sección de estilos
- Ajusta el zoom del mapa
- Agrega más categorías

### Desplegar

Cuando estés listo para llevar a producción:

1. Lee [DEPLOYMENT.md](DEPLOYMENT.md)
2. Elige tu plataforma preferida
3. Sigue las instrucciones

---

## 📞 Necesitas Ayuda?

- 📖 Lee [README.md](README.md)
- 🛠️ Ve [SUPABASE_SETUP.md](SUPABASE_SETUP.md)
- 🚀 Ve [DEPLOYMENT.md](DEPLOYMENT.md)
- 🐛 Abre un [Issue](../../issues)

---

## 🎉 ¡Listo!

Tu Tesoros del Barrio está funcionando.

**¿Qué sigue?**

1. Agrega más lugares
2. Invita a amigos
3. Comparte en redes sociales
4. Contribuye al proyecto

¡Disfruta! 🌟

---

**Tiempo total:** ~10-15 minutos  
**Dificultad:** ⭐ Principiante  
**Versión:** 1.0.0
