#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from metodobase import MetodoBase

class Acorralador(MetodoBase):

    __metodo = "acorralador"

    def ejecutar(self):
        """Ejecuta el metodo acorralador de firmas."""
        self._obtener_ruta_completa()
        self.copiar()
        self.modificar(self.__metodo)

    def _obtener_ruta_completa(self):
        """Obtiene la ruta completa del archivo modificado."""
        nombre, extension = os.path.splitext(self.infile)
        self.outfile = "_acorralado".join((nombre, extension))