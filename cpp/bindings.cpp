#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "Encriptador.h"

namespace py = pybind11;

PYBIND11_MODULE(encriptador, m) {
    m.doc() = "Módulo de encriptación y desencriptación basado en C++ con soporte para datos binarios.";

    py::class_<Encriptador>(m, "Encriptador")
        .def(py::init<>())  // Constructor por defecto
        .def("encriptar", 
             &Encriptador::encriptar, 
             "Encripta un texto en binario utilizando una clave.",
             py::arg("texto"), 
             py::arg("clave"))
        .def("desencriptar", 
             &Encriptador::desencriptar, 
             "Desencripta un texto binario utilizando una clave.",
             py::arg("texto_encriptado"), 
             py::arg("clave"));
}
