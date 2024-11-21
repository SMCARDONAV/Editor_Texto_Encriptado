#ifndef ENCRIPTADOR_H
#define ENCRIPTADOR_H

#include <string>

class Encriptador {
public:
    std::string encriptar(const std::string &texto, const std::string &clave);
    std::string desencriptar(const std::string &textoEncriptado, const std::string &clave);
};

#endif 