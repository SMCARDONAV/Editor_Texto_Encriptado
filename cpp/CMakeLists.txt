cmake_minimum_required(VERSION 3.10)
project(EditorTextoEncriptado)

# Configuración del estándar de C++
set(CMAKE_CXX_STANDARD 17)

# Buscar bibliotecas necesarias
find_package(CryptoPP REQUIRED)
find_package(pybind11 REQUIRED)

# Crear la biblioteca compartida para Python
pybind11_add_module(encriptador bindings.cpp Encriptador.cpp)
target_link_libraries(encriptador PRIVATE cryptopp)

# Crear un ejecutable para pruebas en C++
add_executable(main main.cpp Encriptador.cpp)
target_link_libraries(main PRIVATE cryptopp)

