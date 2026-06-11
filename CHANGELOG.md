# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2024-01-15

### Agregado

- ✨ **Autenticación de Usuarios**
  - Registro con email y contraseña
  - Login seguro con Supabase Auth
  - Recuperación de sesión
  - Cierre de sesión

- 🗺️ **Mapa Interactivo**
  - Mapa base con Folium
  - Marcadores interactivos para cada lugar
  - Popups con información detallada
  - Zoom automático

- 📍 **Gestión de Lugares**
  - Crear nuevos lugares
  - Editar lugares propios
  - Eliminar lugares propios
  - Visualizar todos los lugares
  - 6 categorías predefinidas (Parque, Heladería, Mural, Mascotas, Lugar secreto, Otro)

- 📸 **Almacenamiento de Imágenes**
  - Subida de fotos a Supabase Storage
  - Validación de tipo y tamaño
  - Visualización de imágenes en mapas y tarjetas

- 🔍 **Exploración y Filtrado**
  - Filtrar por categoría
  - Filtrar por usuario
  - Vista de mapa con filtros
  - Vista de exploración con detalles

- ⚙️ **Configuración de Usuario**
  - Panel de perfil
  - Estadísticas personales
  - Selección de tema
  - Información sobre la aplicación

- 🔒 **Seguridad**
  - Row Level Security (RLS) en todas las tablas
  - Autenticación con Supabase
  - Validación de permisos lado servidor
  - Encriptación de contraseñas

- 📊 **Base de Datos**
  - Tablas normalizadas (usuarios, lugares, logs_actividad)
  - Índices para optimización
  - Triggers para auditoría
  - Funciones de seguridad

- 📚 **Documentación**
  - README completo
  - Guía de instalación
  - Guía de configuración de Supabase
  - Guía de despliegue
  - Guía de contribución

- 🐳 **Despliegue**
  - Dockerfile para contenedor
  - docker-compose.yml
  - Procfile para Heroku
  - Configuración para Streamlit Cloud
  - Soporte para Railway, Render, Google Cloud Run, AWS Beanstalk

### Cambios

- Diseño modular con separación de responsabilidades
- Código comentado y documentado
- Estilos CSS personalizados para mejor UX
- Interfaz responsive y mobile-friendly

### Seguridad

- Implementación completa de RLS
- Validación de entrada
- Protección contra CSRF
- Manejo seguro de credenciales

## [Planificado para Futuras Versiones]

### v1.1.0 (Próximamente)

- [ ] Búsqueda por proximidad geográfica
- [ ] Sistema de ratings/valoraciones
- [ ] Comentarios en lugares
- [ ] Geolocalización automática
- [ ] Modo offline
- [ ] Notificaciones en tiempo real

### v1.2.0

- [ ] Integración con redes sociales (compartir)
- [ ] Galería de fotos múltiples por lugar
- [ ] Edición de coordenadas en el mapa
- [ ] Favoritos/bookmarks
- [ ] Historial de cambios

### v2.0.0

- [ ] App móvil nativa (React Native)
- [ ] Sistema de comunidades
- [ ] Eventos en lugares
- [ ] Sistema de puntos/gamificación
- [ ] Integración con mapas de Google

---

## Cómo Reportar Cambios

Si deseas proponer un cambio para futuras versiones:

1. Abre un [Issue](../../issues) o [Discussion](../../discussions)
2. Describe la funcionalidad deseada
3. Explica el caso de uso
4. Aguarda feedback de los mantainers

---

## Versiones Anteriores

### [0.9.0] - Beta (Nunca lanzada públicamente)

- Versión inicial de desarrollo
- Funcionalidades básicas

---

**Versión Actual:** 1.0.0  
**Fecha de Lanzamiento:** 15 de Enero de 2024  
**Estado:** ✅ Producción
