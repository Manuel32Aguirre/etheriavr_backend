0. Verificar si docker esta corriendo
0.1. Hacer un: docker compose down -v
1.Levatamos el contenedor que tiene la base de datos en MySQL
docker compose up --build --detach
2.Levantamos el backend
python main.py
3. Ejecutar la aplicación de escritorio
python main.py

## Modo local vs despliegue (AWS EC2)

El backend ahora soporta una bandera para desactivar automaticamente el descubrimiento UDP en nube:

- `IS_DEPLOYMENT=False` y `ENABLE_UDP_BEACON=True`: modo local con descubrimiento en LAN.
- `IS_DEPLOYMENT=True` y `ENABLE_UDP_BEACON=False`: modo despliegue (recomendado en EC2).

En EC2 usa al menos:

```
IS_DEPLOYMENT=True
ENABLE_UDP_BEACON=False
DEBUG_MODE=False
```