#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random

class MetodoBase(object):

    def __init__(self, archivo, data, opciones, directorio=None):
        self.infile = archivo
        self.directorio = directorio

        # Data
        self.primer_offset = data.obtener_primer_offset()
        self.ultimo_offset = data.obtener_ultimo_offset()
        self.bytes = data.obtener_bytes()
        self.relleno = data.obtener_relleno()

        # Opciones
        self.__vaciar_directorio = opciones.obtener_vaciar_directorio()
        self.__relleno_aleatorio = opciones.obtener_relleno_aleatorio()

    def obtener_ruta_completa(self):
        """Obtiene la ruta completa del archivo modificado."""
        nombre = "{0}_{1}".format(self.primer_offset, self.bytes)
        extension = os.path.splitext(self.infile)[-1]
        archivo = nombre + extension
        self.outfile = os.path.join(self.directorio, archivo)

    def copiar(self, bytes=None):
        """Crea una copia del archivo original."""
        with open(self.infile, "rb") as infile:
            with open(self.outfile, "wb") as outfile:
                if bytes:
                    outfile.write(infile.read(bytes))
                else:
                    outfile.write(infile.read())

    def modificar(self, metodo):
        """Modifica el archivo copiado."""
        inicio = self.primer_offset
        if metodo == "avfucker":
            fin = inicio + self.bytes
        elif metodo == "acorralador":
            fin = self.ultimo_offset + 1
        with open(self.outfile, "r+b") as f:
            for i in range(inicio, fin):
                f.seek(i)
                f.write(self.relleno)

    ############
    # OPCIONES #
    ############

    def vaciar_directorio(self):
        """Borra los archivos contenidos dentro del directorio de trabajo."""
        if not self.__vaciar_directorio:
            return
        archivos = os.listdir(self.directorio)
        for archivo in archivos:
            archivo = os.path.join(self.directorio, archivo)
            os.remove(archivo)

    def relleno_aleatorio(self):
        """Crea un byte de relleno aleatorio."""
        if not self.__relleno_aleatorio:
            return
        num = randint(0, 255)
        self.relleno = hex(num)[2:].zfill(2).decode("hex")