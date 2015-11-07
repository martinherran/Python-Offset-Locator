#!/usr/bin/env python
# -*- coding: utf-8 -*-

from metodobase import MetodoBase

class AVFucker(MetodoBase):

    __metodo = "avfucker"

    def ejecutar(self):
        """Ejecuta el método avfucker."""
        self.vaciar_directorio()
        while self.primer_offset <= self.ultimo_offset:
            self.obtener_ruta_completa()
            self.copiar()
            self.modificar(self.__metodo)
            self.primer_offset += self.bytes