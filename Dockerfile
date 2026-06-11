FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requisitos
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio de configuración de Streamlit
RUN mkdir -p ~/.streamlit

# Crear archivo de configuración de Streamlit
RUN echo "[server]" > ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "enableXsrfProtection = false" >> ~/.streamlit/config.toml && \
    echo "[theme]" >> ~/.streamlit/config.toml && \
    echo "primaryColor = \"#2d7d4d\"" >> ~/.streamlit/config.toml && \
    echo "backgroundColor = \"#ffffff\"" >> ~/.streamlit/config.toml

# Exponer puerto
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py", "--logger.level=error"]
