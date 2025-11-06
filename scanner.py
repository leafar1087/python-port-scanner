# Proyecto: Escáner de Puertos Básico
# Lección 1.1: Comprobar un solo puerto

# 1. Importamos la librería 'socket' (para conexiones de red)
#    y 'sys' (para salir del script si hay un error)
import socket
import sys

print("--- Iniciando Escáner de Puertos v0.1 ---")

# 2. Definimos nuestro objetivo
#    (Usaremos un host fácil de probar, como google.com)
#    (Para probar en tu propia máquina, usa '127.0.0.1')
ip_objetivo = '142.250.184.78' # Esta es una de las IPs de google.com
puerto_objetivo = 80        # El puerto 80 es para HTTP (web)

print(f"Intentando conectar a {ip_objetivo} en el puerto {puerto_objetivo}...")

# 3. ¡Aquí empieza la lógica de red!
try:
    # 4. Creamos el "enchufe" (el objeto socket)
    #    AF_INET = Usaremos el protocolo de internet IPv4 (ej. 1.2.3.4)
    #    SOCK_STREAM = Usaremos el protocolo TCP (el más común, fiable)
    mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 5. Establecemos un tiempo de espera (¡CRÍTICO!)
    #    Si no responde en 1 segundo, asumimos que no funciona.
    mi_socket.settimeout(1.0) # 1.0 segundos

    # 6. Intentamos "conectar el enchufe"
    #    connect_ex() devuelve 0 si tiene ÉXITO (puerto abierto)
    #    y un código de error si falla (puerto cerrado).
    resultado = mi_socket.connect_ex((ip_objetivo, puerto_objetivo))

    # 7. Usamos la lógica 'if' que ya conocemos
    if resultado == 0:
        print(f"[ÉXITO] ¡El puerto {puerto_objetivo} está ABIERTO!")
    else:
        print(f"[FALLO] El puerto {puerto_objetivo} está CERRADO (Código: {resultado})")

except socket.error as e:
    # 8. 'except' por si la IP no existe o algo más falla
    print(f"[ERROR] Ocurrió un error de socket: {e}")
except KeyboardInterrupt:
    # Para poder parar el script con Ctrl+C
    print("\n[INFO] Escaneo cancelado por el usuario.")
    sys.exit()

finally:
    # 9. ¡Limpieza! (Fundamental)
    # Cerramos el "enchufe", hayamos tenido éxito o no.
    mi_socket.close()
    print("--- Conexión cerrada. Escaneo finalizado ---")