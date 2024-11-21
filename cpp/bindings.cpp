#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "Encriptador.h"

namespace py = pybind11;

PYBIND11_MODULE(encriptador, m) {
    py::class_<Encriptador>(m, "Encriptador")
        .def(py::init<>())  // Constructor
        .def("encriptar", &Encriptador::encriptar, "Encripta un texto con una clave",
             py::arg("texto"), py::arg("clave"))
        .def("desencriptar", &Encriptador::desencriptar, "Desencripta un texto con una clave",
             py::arg("texto_encriptado"), py::arg("clave"));
}
