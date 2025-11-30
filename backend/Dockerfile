# Usamos una imagen ligera de Python
FROM python:3.10-slim

# Evita que Python guarde archivos caché (.pyc)
ENV PYTHONDONTWRITEBYTECODE 1
# Hace que los mensajes de log salgan directos a la consola
ENV PYTHONUNBUFFERED 1

# Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instalamos las herramientas del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos los requisitos e instalamos
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiamos todo el código del backend
COPY . /app/

# Este comando se ejecutará al arrancar
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]