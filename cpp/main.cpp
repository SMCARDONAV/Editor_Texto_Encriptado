#include <iostream>
#include <fstream>
#include <vector>
#include "Encriptador.h"

// Guardar datos en un archivo binario
void guardarEnArchivo(const std::string &nombreArchivo, const std::vector<unsigned char> &contenido) {
    std::ofstream archivo(nombreArchivo, std::ios::binary);
    if (!archivo) {
        std::cerr << "Error al abrir el archivo para escribir.\n";
        return;
    }
    archivo.write(reinterpret_cast<const char*>(contenido.data()), contenido.size());
    archivo.close();
    std::cout << "Archivo guardado exitosamente: " << nombreArchivo << "\n";
}

// Leer datos desde un archivo binario
std::vector<unsigned char> leerDesdeArchivo(const std::string &nombreArchivo) {
    std::ifstream archivo(nombreArchivo, std::ios::binary);
    if (!archivo) {
        std::cerr << "Error al abrir el archivo para leer.\n";
        return {};
    }
    std::vector<unsigned char> contenido((std::istreambuf_iterator<char>(archivo)), std::istreambuf_iterator<char>());
    archivo.close();
    return contenido;
}

int main() {
    Encriptador encriptador;

    // Clave de encriptación/desencriptación (32 caracteres para AES-256)
    std::string clave = "mysecurepassword1234567890123456";

    // Texto a encriptar
    std::string texto_original = "Este es un texto de prueba para guardar en un archivo encriptado.";

    try {
        // Encriptar el texto
        std::vector<unsigned char> texto_encriptado = encriptador.encriptar(texto_original, clave);
        std::cout << "Texto encriptado (en bytes): ";
        for (unsigned char c : texto_encriptado) {
            std::cout << std::hex << static_cast<int>(c) << " ";
        }
        std::cout << "\n";

        // Guardar el texto encriptado en un archivo
        std::string archivoEncriptado = "data/prueba1.enc";
        guardarEnArchivo(archivoEncriptado, texto_encriptado);

        // Leer el texto encriptado desde el archivo
        std::vector<unsigned char> texto_encriptado_leido = leerDesdeArchivo(archivoEncriptado);
        if (texto_encriptado_leido.empty()) {
            std::cerr << "No se pudo leer el archivo encriptado.\n";
            return 1;
        }

        // Desencriptar el texto leído
        std::string texto_desencriptado = encriptador.desencriptar(texto_encriptado_leido, clave);
        std::cout << "Texto desencriptado:\n" << texto_desencriptado << "\n";

    } catch (const std::exception &e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }

    return 0;
}
