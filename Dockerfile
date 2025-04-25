FROM python:3.10-slim

# Instalar Tesseract y librerías necesarias
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar primero requirements.txt para aprovechar la cache de Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Ahora copiar el resto del código
COPY . /app/

# Crear directorio de uploads
RUN mkdir -p uploads && chmod 777 uploads

EXPOSE 5000

# Usar variable de entorno para puerto
ENV PORT=5000

# Comando para iniciar la aplicación
CMD ["python", "app.py"]