#include "Encriptador.h"
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <stdexcept>
#include <vector>
#include <cstring>

Encriptador::Encriptador() {}

std::vector<unsigned char> Encriptador::encriptar(const std::string& texto, const std::string& clave) {
    const EVP_CIPHER* cipher = EVP_aes_256_cbc();
    unsigned char iv[EVP_MAX_IV_LENGTH];
    if (!RAND_bytes(iv, sizeof(iv))) {
        throw std::runtime_error("Error generando IV");
    }

    std::vector<unsigned char> ciphertext(texto.size() + EVP_CIPHER_block_size(cipher) + sizeof(iv));
    std::memcpy(ciphertext.data(), iv, sizeof(iv));

    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    if (!ctx) {
        throw std::runtime_error("Error creando contexto de encriptación");
    }

    if (EVP_EncryptInit_ex(ctx, cipher, nullptr, reinterpret_cast<const unsigned char*>(clave.data()), iv) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Error inicializando encriptación");
    }

    int len;
    if (EVP_EncryptUpdate(ctx, ciphertext.data() + sizeof(iv), &len,
                          reinterpret_cast<const unsigned char*>(texto.data()), texto.size()) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Error encriptando datos");
    }

    int final_len;
    if (EVP_EncryptFinal_ex(ctx, ciphertext.data() + sizeof(iv) + len, &final_len) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Error finalizando encriptación");
    }

    ciphertext.resize(sizeof(iv) + len + final_len);
    EVP_CIPHER_CTX_free(ctx);

    return ciphertext;
}

std::string Encriptador::desencriptar(const std::vector<unsigned char>& texto_encriptado, const std::string& clave) {
    const EVP_CIPHER* cipher = EVP_aes_256_cbc();
    const unsigned char* iv = texto_encriptado.data();

    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    if (!ctx) {
        throw std::runtime_error("Error creando contexto de desencriptación");
    }

    if (EVP_DecryptInit_ex(ctx, cipher, nullptr, reinterpret_cast<const unsigned char*>(clave.data()), iv) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Error inicializando desencriptación");
    }

    std::vector<unsigned char> plaintext(texto_encriptado.size() - EVP_MAX_IV_LENGTH);
    int len;
    if (EVP_DecryptUpdate(ctx, plaintext.data(), &len, texto_encriptado.data() + EVP_MAX_IV_LENGTH,
                          texto_encriptado.size() - EVP_MAX_IV_LENGTH) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Error desencriptando datos");
    }

    int final_len;
    if (EVP_DecryptFinal_ex(ctx, plaintext.data() + len, &final_len) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Error finalizando desencriptación");
    }

    plaintext.resize(len + final_len);
    EVP_CIPHER_CTX_free(ctx);

    return std::string(plaintext.begin(), plaintext.end());
}
