# Proyecto: Escáner de Puertos Básico
# Lección 1.4: Herramienta Multihilo (Rápida)

import socket
import sys
import argparse
import threading  # ¡NUEVA IMPORTACIÓN para hilos!
from queue import Queue   # ¡NUEVA IMPORTACIÓN para la cola de tareas!

# --- Función de Escaneo (sin cambios) ---
# Esta es la función que ejecutará CADA hilo
def escanear_puerto(ip_objetivo, puerto):
    """
    Intenta conectar a un puerto específico.
    Devuelve True si está abierto, False si está cerrado.
    """
    try:
        mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mi_socket.settimeout(0.5)
        resultado = mi_socket.connect_ex((ip_objetivo, puerto))
        mi_socket.close()
        return resultado == 0
    except socket.error:
        return False
    # Nota: Quitamos el KeyboardInterrupt de aquí
    # para manejarlo solo en el bucle principal.

# --- 1. ¡NUEVA FUNCIÓN "TRABAJADOR"! ---
# Este es el "manual de instrucciones" que seguirá cada uno de nuestros hilos.
def trabajador(q, ip_objetivo, puertos_abiertos, lock_impresion):
    """Toma puertos de la cola y los escanea."""
    while True:
        try:
            # 2. Toma un puerto de la "fila" (cola)
            # q.get() es "bloqueante": si la cola está vacía, espera.
            puerto = q.get()
            
            # 3. Escanea ese puerto
            if escanear_puerto(ip_objetivo, puerto):
                # 4. ¡USAMOS EL CANDADO!
                # 'with' adquiere el candado antes de imprimir/añadir
                # y lo suelta automáticamente al salir del bloque.
                with lock_impresion:
                    print(f"[ÉXITO] ¡El puerto {puerto} está ABIERTO!")
                    puertos_abiertos.append(puerto)
                    
        except Exception as e:
            # En caso de un error inesperado en el hilo
            print(f"Error en el hilo: {e}")
            
        finally:
            # 5. ¡Contabilidad! Avisa a la cola que esta tarea terminó.
            q.task_done()

# -----------------------------------------------------------------
# --- FUNCIÓN PRINCIPAL (main) ---
# -----------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Escáner de Puertos Multihilo en Python")
    parser.add_argument("-H", "--host", required=True, help="El host o IP a escanear")
    parser.add_argument("-p", "--ports", required=True, help="El rango de puertos (ej. '1-1024')")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Número de hilos (trabajadores) (default: 100)")
    args = parser.parse_args()
    
    host_objetivo = args.host
    rango_string = args.ports
    num_hilos = args.threads

    print("--- Iniciando Escáner de Puertos v0.5 (Multihilo) ---")

    # --- Resolución DNS ---
    try:
        ip_objetivo = socket.gethostbyname(host_objetivo)
        print(f"IP resuelta: {ip_objetivo}")
    except socket.gaierror:
        print(f"[ERROR] No se pudo resolver el nombre de host: {host_objetivo}")
        sys.exit()

    # --- Parseo del Rango (¡Lo ponemos en un try...except!) ---
    try:
        partes = rango_string.split('-')
        puerto_inicial = int(partes[0])
        puerto_final = int(partes[1])
        if puerto_inicial > puerto_final: raise ValueError
    except:
        print("[ERROR] Rango de puertos inválido. Use: '1-1024'")
        sys.exit()

    # --- 6. Creación de la Cola y el Candado ---
    puerto_queue = Queue()
    puertos_abiertos = []
    lock_impresion = threading.Lock()

    print(f"Lanzando {num_hilos} hilos para escanear de {puerto_inicial} a {puerto_final}...")

    # --- 7. "Contratamos" y lanzamos los hilos (trabajadores) ---
    for _ in range(num_hilos):
        t = threading.Thread(
            target=trabajador, # Diles que sigan el manual 'trabajador'
            args=(puerto_queue, ip_objetivo, puertos_abiertos, lock_impresion),
            daemon=True # 'daemon=True' significa que el hilo morirá si el script principal termina
        )
        t.start()

    # --- 8. Llenamos la "fila" (cola) con todas las tareas ---
    try:
        for puerto in range(puerto_inicial, puerto_final + 1):
            puerto_queue.put(puerto)
        
        # 9. ¡Esperamos a que la cola se vacíe!
        # q.join() pausa el script principal aquí
        # hasta que se llame a q.task_done() por cada ítem.
        puerto_queue.join()
        
    except KeyboardInterrupt:
        print("\n[INFO] Escaneo cancelado por el usuario.")
        sys.exit()

    # --- 10. Reporte Final ---
    print("\n--- Escaneo Completo ---")
    if puertos_abiertos:
        print("Puertos abiertos encontrados (ordenados):")
        puertos_abiertos.sort() # Ordenamos la lista
        print(puertos_abiertos)
    else:
        print("No se encontraron puertos abiertos en el rango especificado.")

# --- Punto de Entrada ---
if __name__ == "__main__":
    main()