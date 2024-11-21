#ifndef ENCRIPTADOR_H
#define ENCRIPTADOR_H

#include <string>
#include <vector>

class Encriptador {
public:
    Encriptador();
    std::vector<unsigned char> encriptar(const std::string& texto, const std::string& clave);
    std::string desencriptar(const std::vector<unsigned char>& texto_encriptado, const std::string& clave);
};

#endif // ENCRIPTADOR_H
