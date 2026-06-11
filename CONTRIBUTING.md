# Guía de Contribución

¡Gracias por interesarte en contribuir a Tesoros del Barrio! 🎉

Todos los niveles de experiencia son bienvenidos. Esta guía te ayudará a entender cómo contribuir.

## 📋 Código de Conducta

Por favor, sé respetuoso y constructivo en todas las interacciones.

## 🐛 Reportar Bugs

Si encuentras un bug:

1. **Verifica** que no haya sido reportado ya en [Issues](../../issues)
2. **Crea un nuevo issue** con:
   - Título claro del problema
   - Descripción detallada
   - Pasos para reproducir
   - Resultado esperado
   - Resultado actual
   - Tu entorno (SO, versión Python, etc.)

### Ejemplo

```
Título: Login falla con emails que tienen números

Descripción:
Cuando intento registrarme con un email como "usuario123@gmail.com",
la aplicación muestra un error.

Pasos:
1. Ir a la pantalla de registro
2. Ingresar "usuario123@gmail.com" como email
3. Ingresar contraseña
4. Hacer clic en Registrarse

Resultado esperado:
Registro exitoso

Resultado actual:
Error: Invalid email format

Entorno:
- OS: Windows 10
- Python: 3.11.0
- Streamlit: 1.38.0
```

## 🎨 Sugerir Mejoras

¿Tienes una idea?

1. Abre un [Issue](../../issues) con el label `enhancement`
2. Describe la mejora
3. Explica por qué crees que es útil
4. Muestra ejemplos si es posible

## 🔄 Contribuir Código

### 1. Fork el Repositorio

```bash
git clone https://github.com/tu-usuario/tesoros-del-barrio.git
cd tesoros-del-barrio
```

### 2. Crear Rama Feature

```bash
# Actualiza main
git checkout main
git pull origin main

# Crea rama para tu feature
git checkout -b feature/descripcion-feature

# Ejemplo
git checkout -b feature/agregar-filtro-por-proximidad
```

### 3. Hacer Cambios

- Sigue el estilo de código existente
- Comenta código complejo
- Actualiza la documentación si es necesario

### 4. Probar Cambios

```bash
# Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instala dependencias
pip install -r requirements.txt

# Ejecuta la aplicación
streamlit run app.py
```

### 5. Commit y Push

```bash
# Agrega cambios
git add .

# Commit con mensaje descriptivo
git commit -m "Agrega filtro por proximidad en el mapa"

# Push a tu fork
git push origin feature/descripcion-feature
```

### 6. Pull Request

1. Ve a tu fork en GitHub
2. Haz clic en "Compare & pull request"
3. Describe los cambios
4. Haz clic en "Create pull request"

### Estructura de Commits

Usa mensajes descriptivos:

```
[Tipo] Descripción corta

Descripción más detallada si es necesario
```

Tipos:
- `[Feature]` - Nueva funcionalidad
- `[Fix]` - Corrección de bug
- `[Docs]` - Cambios en documentación
- `[Style]` - Formato de código
- `[Test]` - Pruebas
- `[Refactor]` - Refactorización

### Ejemplos

```
[Feature] Agregar búsqueda por nombre de lugar

Permite a los usuarios buscar lugares por nombre
en el campo de exploración.

[Fix] Corregir error al eliminar lugares sin foto

Las imágenes opcional ahora se manejan correctamente.

[Docs] Actualizar README con ejemplos

Se agregaron ejemplos de uso en la sección de instalación.
```

## 📝 Estilos de Código

### Python

```python
# Usa nombres descriptivos
def obtener_lugares_por_categoria(categoria):
    """
    Obtiene lugares de una categoría específica.
    
    Args:
        categoria (str): Categoría a filtrar
        
    Returns:
        list: Lista de lugares
    """
    # Implementación
    pass

# Comenta lógica compleja
# Usa type hints cuando sea posible
def procesar_coordenadas(lat: float, lon: float) -> bool:
    """Valida coordenadas geográficas."""
    return -90 <= lat <= 90 and -180 <= lon <= 180
```

### Streamlit Components

```python
# Agrupa componentes relacionados
with st.sidebar:
    st.header("Opciones")
    
    categoria = st.selectbox(
        "Categoría",
        ["Parque", "Heladería", "Mural"]
    )

# Usa containers para mejor organización
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Métrica", valor)
```

## 📚 Documentación

Si agregas una feature, por favor:

1. Documenta el código
2. Actualiza el README.md si es necesario
3. Agrega ejemplos de uso
4. Actualiza CHANGELOG.md

### Docstring Template

```python
def mi_funcion(parametro1: str, parametro2: int) -> bool:
    """
    Descripción breve de qué hace la función.
    
    Descripción más larga si es necesario, explicando
    el comportamiento, casos especiales, etc.
    
    Args:
        parametro1 (str): Descripción del parámetro
        parametro2 (int): Descripción del parámetro
        
    Returns:
        bool: Descripción del valor retornado
        
    Raises:
        ValueError: Cuándo se lanza esta excepción
        
    Example:
        >>> resultado = mi_funcion("texto", 42)
        >>> print(resultado)
        True
    """
    pass
```

## 🧪 Testing

Aunque actualmente no hay tests automatizados, puedes:

1. Probar tu feature manualmente
2. Verificar que no rompe funcionalidad existente
3. Documentar los pasos de prueba en tu PR

### Checklist de Testing

- [ ] Funciona en navegadores principales (Chrome, Firefox, Safari)
- [ ] Se ve bien en mobile
- [ ] Sin errores en la consola
- [ ] Las imágenes se cargan correctamente
- [ ] La autenticación funciona
- [ ] El mapa se muestra correctamente

## 🚀 Proceso de Review

Los PRs serán revisados por los mantainers:

1. Se revisará el código
2. Se pueden solicitar cambios
3. Una vez aprobado, se mergeará a `main`
4. Se agregará a la próxima release

## 📖 Recursos Útiles

- [Documentación Streamlit](https://docs.streamlit.io)
- [Documentación Supabase](https://supabase.com/docs)
- [Documentación Folium](https://python-visualization.github.io/folium/)
- [Git Guide](https://git-scm.com/doc)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)

## 💬 Preguntas?

- Abre una [Discussion](../../discussions)
- Contacta a los mantainers
- Revisa issues cerrados para ver si ya se respondió

## 🎯 Áreas Donde Necesitamos Ayuda

- ✅ Traducción a otros idiomas
- ✅ Mejoras de UI/UX
- ✅ Optimización de rendimiento
- ✅ Tests automatizados
- ✅ Documentación
- ✅ Correcciones de bugs

¡Gracias por contribuir! 🌟

---

**Último actualizado:** 2024  
**Versión:** 1.0
