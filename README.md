# Escáner de Puertos Multihilo en Python

Un escáner de puertos rápido y eficiente implementado en Python que utiliza programación multihilo para escanear múltiples puertos simultáneamente.

## 📋 Descripción

Este proyecto es una herramienta de escaneo de puertos que permite identificar qué puertos están abiertos en un host objetivo. Utiliza programación multihilo para mejorar significativamente el rendimiento comparado con escaneos secuenciales tradicionales.

## ✨ Características

- **Escaneo multihilo**: Utiliza múltiples hilos para escanear puertos en paralelo
- **Rango de puertos personalizable**: Permite especificar un rango de puertos a escanear
- **Resolución DNS**: Soporta tanto direcciones IP como nombres de dominio
- **Configuración de hilos**: Permite ajustar el número de hilos trabajadores
- **Manejo de errores**: Gestión robusta de errores y excepciones
- **Interrupción segura**: Soporte para cancelación con Ctrl+C

## 🔧 Requisitos

- Python 3.6 o superior
- Módulos estándar de Python (no se requieren dependencias externas):
  - `socket`
  - `threading`
  - `queue`
  - `argparse`

## 📦 Instalación

1. Clona o descarga este repositorio:
```bash
git clone <url-del-repositorio>
cd PYTHON-PORT-SCANNER
```

2. No se requiere instalación de dependencias adicionales, ya que el proyecto utiliza solo módulos estándar de Python.

## 🚀 Uso

### Sintaxis básica

```bash
python python-port-scanner/scanner.py -H <host> -p <rango-puertos> [-t <número-hilos>]
```

### Parámetros

- `-H, --host` (requerido): El host o IP a escanear
- `-p, --ports` (requerido): El rango de puertos en formato `inicio-fin` (ej. `1-1024`)
- `-t, --threads` (opcional): Número de hilos trabajadores (por defecto: 100)

### Ejemplos

#### Escanear puertos comunes en localhost
```bash
python python-port-scanner/scanner.py -H localhost -p 1-1024
```

#### Escanear un rango específico en una IP
```bash
python python-port-scanner/scanner.py -H 192.168.1.1 -p 20-80
```

#### Escanear con un número personalizado de hilos
```bash
python python-port-scanner/scanner.py -H example.com -p 1-1000 -t 200
```

#### Escanear puertos comunes en un servidor web
```bash
python python-port-scanner/scanner.py -H google.com -p 80-443
```

## 📁 Estructura del Proyecto

```
PYTHON-PORT-SCANNER/
├── python-port-scanner/
│   └── scanner.py          # Script principal del escáner
└── README.md               # Este archivo
```

## 🔍 Cómo Funciona

1. **Resolución DNS**: El script resuelve el nombre de host a una dirección IP
2. **Creación de hilos**: Se crean múltiples hilos trabajadores según el parámetro especificado
3. **Cola de tareas**: Los puertos a escanear se colocan en una cola (Queue)
4. **Escaneo paralelo**: Cada hilo toma puertos de la cola y los escanea simultáneamente
5. **Sincronización**: Se utiliza un candado (Lock) para evitar condiciones de carrera al imprimir resultados
6. **Reporte**: Al finalizar, se muestra una lista ordenada de puertos abiertos

## ⚠️ Notas Importantes

- **Uso ético**: Este software es solo para fines educativos y pruebas de seguridad autorizadas. No lo uses en sistemas sin permiso explícito.
- **Timeout**: Cada conexión tiene un timeout de 0.5 segundos
- **Rendimiento**: El número óptimo de hilos depende de tu sistema y la red. 100 hilos es un buen punto de partida.
- **Interrupción**: Puedes cancelar el escaneo en cualquier momento con `Ctrl+C`

## 🐛 Solución de Problemas

### Error: "No se pudo resolver el nombre de host"
- Verifica que el nombre de host o IP sea correcto
- Asegúrate de tener conexión a internet si estás resolviendo un dominio

### Error: "Rango de puertos inválido"
- Asegúrate de usar el formato correcto: `inicio-fin` (ej. `1-1024`)
- El puerto inicial debe ser menor o igual al puerto final

### El escaneo es muy lento
- Aumenta el número de hilos con el parámetro `-t`
- Ten en cuenta que demasiados hilos pueden saturar tu sistema

## 📝 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

## 👨‍💻 Autor

Desarrollado por Rafael Pérez

LinkedIn: [https://www.linkedin.com/in/rperezll/]
GitHub: [https://github.com/leafar1087]

Proyecto educativo de escaneo de puertos con programación multihilo.

---

**Versión**: 0.5 (Multihilo)

