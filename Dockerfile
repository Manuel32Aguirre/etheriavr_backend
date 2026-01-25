# 1. Usamos una imagen ligera de Python 3.12
FROM python:3.12

# 2. Evitamos que Python genere los archivos .pycache
ENV PYTHONDONTWRITEBYTECODE=1
# 3. Evita que Python guarde logs en el buffer para verlos en tiempo real
ENV PYTHONUNBUFFERED=1

# 4. Definimos dónde va a vivir el código dentro del contenedor
WORKDIR /app

# 5. Instalamos las dependencias
# (Asegúrate de tener un archivo requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el resto de tu código
COPY . .

# 7. El comando para arrancar tu API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]