0. Verificar si docker esta corriendo
0.1. Hacer un: docker compose down -v
1.Levatamos el contenedor que tiene la base de datos en MySQL
docker compose up --build --detach
2.Levantamos el backend
python main.py
3. Ejecutar la aplicación de escritorio
python main.py