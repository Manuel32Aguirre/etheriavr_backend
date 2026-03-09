"""
Script de prueba para enviar broadcasts UDP y simular las Quest
"""
import socket
import time

UDP_PORT = 8888
MAGIC_WORD = "ETHERIA_SEARCH"
BROADCAST_IP = "255.255.255.255"

print(f"Enviando broadcast UDP a puerto {UDP_PORT}...")
print(f"Mensaje: {MAGIC_WORD}")
print(f"Presiona CTRL+C para detener\n")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(2.0)

try:
    while True:
        # Enviar broadcast
        sock.sendto(MAGIC_WORD.encode('utf-8'), (BROADCAST_IP, UDP_PORT))
        print(f"[{time.strftime('%H:%M:%S')}] Broadcast enviado, esperando respuesta...")
        
        try:
            # Esperar respuesta
            data, addr = sock.recvfrom(1024)
            response = data.decode('utf-8')
            print(f"✅ RESPUESTA RECIBIDA desde {addr}:")
            print(f"   {response}\n")
        except socket.timeout:
            print(f"❌ No se recibió respuesta (posible firewall bloqueando)\n")
        
        time.sleep(3)
        
except KeyboardInterrupt:
    print("\n\nPrueba finalizada.")
    sock.close()
