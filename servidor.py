import socket
import zlib  # Para checksum

def verificar_checksum(segmento):
    checksum_calculado = zlib.crc32(segmento['datos'].encode())
    return checksum_calculado == segmento['checksum']

def recibir_segmentos(servidor_host, servidor_puerto):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
        servidor.bind((servidor_host, servidor_puerto))
        segmentos_recibidos = []
        while True:
            mensaje, _ = servidor.recvfrom(1024)
            print(f"Mensaje recibido: {mensaje.decode()}")
            segmento = eval(mensaje.decode())
            segmentos_recibidos.append(segmento)
            print(f"Recibido segmento {segmento['numero_secuencia']}")

            if segmento['es_ultimo']:
                break
        return segmentos_recibidos

def ordenar_segmentos(segmentos):
    return sorted(segmentos, key=lambda x: x['numero_secuencia'])

def guardar_datos(segmentos, ruta_archivo):
    with open(ruta_archivo, 'w') as file:
        for segmento in segmentos:
            if verificar_checksum(segmento):
                file.write(segmento['datos'])
            else:
                print(f"Error en el segmento {segmento['numero_secuencia']}: Checksum incorrecto")

# Configuración
SERVIDOR_HOST = '127.0.0.1'
SERVIDOR_PUERTO = 12345
RUTA_ARCHIVO_GUARDADO = 'mensaje_reconstruido.txt'

# Proceso del servidor
segmentos_recibidos = recibir_segmentos(SERVIDOR_HOST, SERVIDOR_PUERTO)
segmentos_ordenados = ordenar_segmentos(segmentos_recibidos)
guardar_datos(segmentos_ordenados, RUTA_ARCHIVO_GUARDADO)