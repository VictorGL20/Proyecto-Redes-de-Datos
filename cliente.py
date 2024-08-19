import socket
import random
import zlib  # Para checksum


def leer_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as file:
        return file.read()


def segmentar_datos(datos, tamano_segmento):
    return [datos[i:i + tamano_segmento] for i in range(0, len(datos), tamano_segmento)]


def encapsular_segmento(segmento, numero_secuencia, es_ultimo):
    checksum = zlib.crc32(segmento.encode())
    return {
        'numero_secuencia': numero_secuencia,
        'checksum': checksum,
        'es_ultimo': es_ultimo,
        'datos': segmento
    }


def simular_errores(segmentos):
    segmentos_con_errores = []
    for segmento in segmentos:
        # Simular pérdida de paquete
        if random.choice([True, False]):
            continue
        # Simular cambios en bits
        if random.choice([True, False]):
            segmento['datos'] = segmento['datos'][:-1] + chr(random.randint(32, 126))
        segmentos_con_errores.append(segmento)

    # Simular envío fuera de orden
    random.shuffle(segmentos_con_errores)
    return segmentos_con_errores


def enviar_segmentos(servidor_host, servidor_puerto, segmentos):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        for segmento in segmentos:
            print(f"Enviando segmento: {segmento}")
            cliente.sendto(str(segmento).encode(), (servidor_host, servidor_puerto))
            print(f"Segmento {segmento['numero_secuencia']} enviado al servidor")


# Configuración
RUTA_ARCHIVO = 'mensaje.txt'
TAMANO_SEGMENTO = 10  # Tamaño de cada segmento
SERVIDOR_HOST = '127.0.0.1'
SERVIDOR_PUERTO = 12345

# Proceso del cliente
datos = leer_archivo(RUTA_ARCHIVO)
segmentos = segmentar_datos(datos, TAMANO_SEGMENTO)
segmentos_encapsulados = [encapsular_segmento(segmentos[i], i, i == len(segmentos) - 1) for i in range(len(segmentos))]
segmentos_con_errores = simular_errores(segmentos_encapsulados)
enviar_segmentos(SERVIDOR_HOST, SERVIDOR_PUERTO, segmentos_con_errores)