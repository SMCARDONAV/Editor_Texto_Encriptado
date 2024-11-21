#include <iostream>
#include <fstream>
#include "Encriptador.h"

void guardarEnArchivo(const std::string &nombreArchivo, const std::string &contenido) {
    std::ofstream archivo(nombreArchivo, std::ios::binary);
    if (!archivo) {
        std::cerr << "Error al abrir el archivo para escribir.\n";
        return;
    }
    archivo.write(contenido.c_str(), contenido.size());
    archivo.close();
    std::cout << "Archivo guardado exitosamente: " << nombreArchivo << "\n";
}

std::string leerDesdeArchivo(const std::string &nombreArchivo) {
    std::ifstream archivo(nombreArchivo, std::ios::binary);
    if (!archivo) {
        std::cerr << "Error al abrir el archivo para leer.\n";
        return "";
    }
    std::string contenido((std::istreambuf_iterator<char>(archivo)), std::istreambuf_iterator<char>());
    archivo.close();
    return contenido;
}

int main() {
    Encriptador encriptador;

    // Clave de encriptación/desencriptación
    std::string clave = "mysecretpassword1234";

    // Texto a encriptar
    std::string texto_original = "Este es un texto de prueba para guardar en un archivo encriptado.";

    // Encriptar el texto
    std::string texto_encriptado = encriptador.encriptar(texto_original, clave);
    std::cout << "Texto encriptado:\n" << texto_encriptado << "\n";

    // Guardar el texto encriptado en un archivo
    std::string archivoEncriptado = "data/prueba1.enc";
    guardarEnArchivo(archivoEncriptado, texto_encriptado);

    // Leer el texto encriptado desde el archivo
    std::string texto_encriptado_leido = leerDesdeArchivo(archivoEncriptado);
    if (texto_encriptado_leido.empty()) {
        std::cerr << "No se pudo leer el archivo encriptado.\n";
        return 1;
    }

    // Desencriptar el texto leído
    std::string texto_desencriptado = encriptador.desencriptar(texto_encriptado_leido, clave);
    std::cout << "Texto desencriptado:\n" << texto_desencriptado << "\n";

    return 0;
}
