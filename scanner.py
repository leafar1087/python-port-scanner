# Proyecto: Escáner de Puertos Básico
# Lección 1.1: Comprobar un solo puerto (versión robusta)

import socket
import sys

print("--- Iniciando Escáner de Puertos v0.2 ---")

# 2. Definimos nuestro objetivo (¡versión mejorada!)
#    Usamos un nombre de host que SÍ quiere ser escaneado
host_objetivo = 'scanme.nmap.org'
puerto_objetivo = 80             # El puerto 80 (HTTP) SÍ está abierto allí

print(f"Objetivo: {host_objetivo}")

# 3. ¡Aquí empieza la lógica de red!
try:
    # 4. ¡NUEVO PASO! Resolvemos el nombre de host a una IP
    #    Esto es como buscar en el directorio telefónico
    ip_objetivo = socket.gethostbyname(host_objetivo)
    print(f"IP resuelta: {ip_objetivo}")

except socket.gaierror:
    # 'gaierror' es el error de "búsqueda de dirección"
    print(f"[ERROR] No se pudo resolver el nombre de host: {host_objetivo}")
    sys.exit() # Salimos del script si no podemos encontrar la IP

print(f"Intentando conectar a {ip_objetivo} en el puerto {puerto_objetivo}...")

try:
    # 5. Creamos el "enchufe" (socket)
    mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mi_socket.settimeout(1.0) # 1.0 segundos

    # 6. Intentamos "conectar el enchufe"
    resultado = mi_socket.connect_ex((ip_objetivo, puerto_objetivo))

    # 7. Usamos la lógica 'if'
    if resultado == 0:
        print(f"[ÉXITO] ¡El puerto {puerto_objetivo} está ABIERTO!")
    else:
        print(f"[FALLO] El puerto {puerto_objetivo} está CERRADO (Código: {resultado})")

except socket.error as e:
    print(f"[ERROR] Ocurrió un error de socket: {e}")
except KeyboardInterrupt:
    print("\n[INFO] Escaneo cancelado por el usuario.")
    sys.exit()

finally:
    # 8. Limpieza
    mi_socket.close()
    print("--- Conexión cerrada. Escaneo finalizado ---")