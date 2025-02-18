# Usa una imagen oficial de Python
FROM python:3.13-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
RUN apt-get update && apt-get install -y libpq-dev gcc


# Crea un usuario no root
#RUN useradd -m django_user
# USER appuser

# Copia los archivos de requisitos
COPY requirements.txt requirements.txt

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación al contenedor
COPY . /app

# Expone el puerto 8000 para Django
# EXPOSE 8000

# Comando por defecto para ejecutar la aplicación
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]