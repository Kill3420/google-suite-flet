FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para Flet
RUN apt-get update && apt-get install -y \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    libgstreamer1.0-0 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer el puerto estándar que usa Render
EXPOSE 10000

# Comando para arrancar Uvicorn apuntando a tu app de FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
