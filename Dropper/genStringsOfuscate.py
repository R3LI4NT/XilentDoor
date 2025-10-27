import base64
import random
import string

def generar_strings_ofuscados(url):
    # Codificar URL en Base64
    url_codificada = base64.b64encode(url.encode()).decode()
    
    print("=" * 60)
    print("GENERADOR DE STRINGS OFUSCADOS")
    print("=" * 60)
    print(f"URL original: {url}")
    print(f"URL en Base64: {url_codificada}")
    print()
    
    # Método 1: División simple
    print("MÉTODO 1 - División simple:")
    print("-" * 30)
    
    partes_simples = dividir_string_simple(url_codificada, 8)
    print("url_parts = [")
    for parte in partes_simples:
        print(f'    "{parte}",')
    print("]")
    print()
    
    # Método 2: División aleatoria
    print("MÉTODO 2 - División aleatoria:")
    print("-" * 30)
    
    partes_aleatorias = dividir_string_aleatorio(url_codificada, 6)
    print("url_parts = [")
    for parte in partes_aleatorias:
        print(f'    "{parte}",')
    print("]")
    print()
    
    # Método 3: Con rotación de caracteres
    print("MÉTODO 3 - Con rotación de caracteres:")
    print("-" * 30)
    
    partes_rotadas = dividir_con_rotacion(url_codificada, 7)
    print("url_parts = [")
    for parte in partes_rotadas:
        print(f'    "{parte}",')
    print("]")
    print()
    

def dividir_string_simple(texto, num_partes):
    longitud = len(texto)
    tamano_parte = longitud // num_partes
    partes = []
    
    for i in range(num_partes):
        inicio = i * tamano_parte
        if i == num_partes - 1:
            fin = longitud
        else:
            fin = inicio + tamano_parte
        partes.append(texto[inicio:fin])
    
    return partes

def dividir_string_aleatorio(texto, num_partes):
    partes = []
    indices = sorted(random.sample(range(1, len(texto)), num_partes - 1))
    indices = [0] + indices + [len(texto)]
    
    for i in range(len(indices) - 1):
        partes.append(texto[indices[i]:indices[i+1]])
    
    return partes

def dividir_con_rotacion(texto, num_partes):
    partes = dividir_string_simple(texto, num_partes)
    partes_rotadas = []
    
    for parte in partes:
        parte_rotada = ''.join(chr((ord(c) + 1) % 127) if c.isprintable() else c for c in parte)
        partes_rotadas.append(parte_rotada)
    
    return partes_rotadas

def decodificar_rotacion(partes_rotadas):
    partes_decodificadas = []
    for parte in partes_rotadas:
        parte_decod = ''.join(chr((ord(c) - 1) % 127) if c.isprintable() else c for c in parte)
        partes_decodificadas.append(parte_decod)
    return "".join(partes_decodificadas)

if __name__ == "__main__":
    print("[+] GENERADOR DE STRINGS OFUSCADOS PARA DROPPERS [+]")
    print()
    
    while True:
        print("Ingresa la URL del archivo (o 'salir' para terminar):")
        url = input("URL: ").strip()
        
        if url.lower() == 'salir':
            break
            
        if not url.startswith(('http://', 'https://')):
            print("[!] Error: La URL debe comenzar con http:// o https://")
            continue

        
        print()
        generar_strings_ofuscados(url)
        print()
        print("=" * 60)
        print()
