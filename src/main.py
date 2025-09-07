"""
Punto de entrada del proyecto.
Se espera que el usuario proporcione un archivo con expresiones regulares.
"""

from utils.io import procesar_archivo

def main():
    archivo = "proyecto.txt"
    procesar_archivo(archivo)

if __name__ == "__main__":
    main()
