import socket
import threading
import os
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()

def start_udp_beacon(api_port):
    # Usamos os.getenv(VARIABLE, VALOR_POR_DEFECTO)
    UDP_PORT = int(os.getenv("UDP_PORT"))
    MAGIC_WORD = os.getenv("MAGIC_WORD")
    SERVER_ID = os.getenv("SERVER_IDENTIFIER")
    DNS_HELPER = os.getenv("DNS_HELPER")

    def beacon_thread():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            sock.bind(('', UDP_PORT))
            print(f"[UDP Beacon] Escuchando en el puerto {UDP_PORT}...")
        except Exception as e:
            print(f"[UDP Beacon] No se pudo bindear el puerto {UDP_PORT}: {e}")
            return

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data.decode('utf-8') == MAGIC_WORD:
                    # Truco para obtener la IP local conectando temporalmente a un DNS externo
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect((DNS_HELPER, 80))
                    local_ip = s.getsockname()[0]
                    s.close()

                    response = f"{SERVER_ID}:{local_ip}:{api_port}"
                    sock.sendto(response.encode('utf-8'), addr)
                    print(f"[UDP Beacon] Quest detectado en {addr}. Respondiendo IP: {local_ip}")
            except Exception as e:
                print(f"[UDP Beacon] Error en loop: {e}")

    thread = threading.Thread(target=beacon_thread, daemon=True)
    thread.start()