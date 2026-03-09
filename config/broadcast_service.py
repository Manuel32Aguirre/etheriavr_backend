import socket
import threading
import os
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()

def get_all_local_ips():
    """Obtiene todas las IPs locales de todas las interfaces de red"""
    ips = []
    try:
        # Obtener el nombre del host
        hostname = socket.gethostname()
        # Obtener todas las IPs asociadas al hostname
        addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET)
        for info in addr_info:
            ip = info[4][0]
            if ip not in ips and not ip.startswith('127.'):
                ips.append(ip)
    except Exception as e:
        print(f"[UDP Beacon] Error obteniendo IPs: {e}")
    return ips

def get_matching_ip(client_addr, available_ips):
    """
    Encuentra la IP del servidor que está en la misma subred que el cliente.
    Esto es crítico cuando hay múltiples interfaces de red activas.
    """
    try:
        # Extraer los primeros 3 octetos del cliente (clase C)
        client_subnet = '.'.join(client_addr.split('.')[:3])
        
        # Buscar una IP del servidor que coincida con la subred del cliente
        for ip in available_ips:
            server_subnet = '.'.join(ip.split('.')[:3])
            if client_subnet == server_subnet:
                return ip
        
        # Si no encuentra coincidencia, devuelve la primera IP disponible
        return available_ips[0] if available_ips else "127.0.0.1"
    except:
        return available_ips[0] if available_ips else "127.0.0.1"

def start_udp_beacon(api_port):
    # Usamos os.getenv(VARIABLE, VALOR_POR_DEFECTO)
    UDP_PORT = int(os.getenv("UDP_PORT"))
    MAGIC_WORD = os.getenv("MAGIC_WORD")
    SERVER_ID = os.getenv("SERVER_IDENTIFIER")

    def beacon_thread():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Habilitar broadcast
        
        try:
            sock.bind(('0.0.0.0', UDP_PORT))  # Escuchar en TODAS las interfaces
            
            # Mostrar todas las IPs disponibles
            local_ips = get_all_local_ips()
            print(f"[UDP Beacon] Escuchando en el puerto {UDP_PORT}")
            print(f"[UDP Beacon] Interfaces de red detectadas:")
            for ip in local_ips:
                print(f"  - {ip}")
            
        except Exception as e:
            print(f"[UDP Beacon] No se pudo bindear el puerto {UDP_PORT}: {e}")
            return

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data.decode('utf-8') == MAGIC_WORD:
                    # Obtener todas las IPs locales
                    local_ips = get_all_local_ips()
                    
                    # Encontrar la IP que está en la misma subred que el cliente
                    local_ip = get_matching_ip(addr[0], local_ips)

                    response = f"{SERVER_ID}:{local_ip}:{api_port}"
                    sock.sendto(response.encode('utf-8'), addr)
                    print(f"[UDP Beacon] Quest detectado en {addr[0]} -> Respondiendo con IP: {local_ip}")
            except Exception as e:
                print(f"[UDP Beacon] Error en loop: {e}")

    thread = threading.Thread(target=beacon_thread, daemon=True)
    thread.start()