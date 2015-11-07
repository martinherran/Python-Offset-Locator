#!/usr/bin/env python
# -*- coding: utf-8 -*-

from metodobase import MetodoBase

class DSplit(MetodoBase):

    __metodo = "dsplit"

    def ejecutar(self):
        """Ejecuta el método dsplit."""
        self.vaciar_directorio()
        while self.primer_offset <= self.ultimo_offset:
            self.obtener_ruta_completa()
            bytes = self.primer_offset + self.bytes
            self.copiar(bytes)
            self.primer_offset += self.bytes