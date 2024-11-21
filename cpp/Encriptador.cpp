#include "Encriptador.h"
#include <crypto++/aes.h>
#include <crypto++/modes.h>
#include <crypto++/filters.h>
#include <stdexcept>

using namespace CryptoPP;

std::string Encriptador::encriptar(const std::string &texto, const std::string &clave) {
    if (clave.size() < AES::DEFAULT_KEYLENGTH) {
        throw std::invalid_argument("La clave debe tener al menos 16 bytes.");
    }

    byte key[AES::DEFAULT_KEYLENGTH];
    std::copy(clave.begin(), clave.begin() + AES::DEFAULT_KEYLENGTH, key);

    byte iv[AES::BLOCKSIZE] = {0x00}; // Vector de inicialización simple
    std::string cipher;

    CBC_Mode<AES>::Encryption encryptor(key, sizeof(key), iv);
    StringSource(texto, true, new StreamTransformationFilter(encryptor, new StringSink(cipher)));

    return cipher;
}

std::string Encriptador::desencriptar(const std::string &textoEncriptado, const std::string &clave) {
    if (clave.size() < AES::DEFAULT_KEYLENGTH) {
        throw std::invalid_argument("La clave debe tener al menos 16 bytes.");
    }

    byte key[AES::DEFAULT_KEYLENGTH];
    std::copy(clave.begin(), clave.begin() + AES::DEFAULT_KEYLENGTH, key);

    byte iv[AES::BLOCKSIZE] = {0x00}; // Vector de inicialización simple
    std::string plain;

    CBC_Mode<AES>::Decryption decryptor(key, sizeof(key), iv);
    StringSource(textoEncriptado, true, new StreamTransformationFilter(decryptor, new StringSink(plain)));

    return plain;
}