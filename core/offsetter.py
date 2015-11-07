#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

class OffSetter(object):

    __offsets = []
    __primer_offset = 1000
    __ultimo_offset = None
    __bytes = 1000
    __relleno = None

    def __init__(self, archivo, debug=False):
        """Configura los datos utilizados por los distintos métodos.

        Atributos:
        offsets -- lista de offsets en formato numérico ([int, int, int])
        primer_offset -- posición del primer offset (int)
        ultimo_offset -- posición del último offset (int)
        bytes -- número de bytes a rellenar (int)
        relleno -- bytes de relleno (int)
        """
        self.__archivo = archivo
        self.__debug = debug
        self._procesar_archivo()

    # PROCESADOR
    def _procesar_archivo(self):
        """Realiza configuración por defecto a partir del análisis del archivo."""
        self._calcular_offsets()
        self._calcular_bytes()
        self.configurar_relleno("90")

    def _calcular_offsets(self):
        """Crea una lista de offsets y obtiene el último offset."""
        archivo = self._validar_archivo(self.__archivo)
        offsets = []

        with open(archivo, "rb") as f:
            cadena_hex = f.read().encode("hex")
            for i in range(len(cadena_hex)):
                if (i % 2) == 0:
                    offset = int(cadena_hex[i:i+2], 16)
                    offsets.append(offset)

        self.__offsets = offsets
        self.__ultimo_offset = len(offsets) - 1
        if self.__ultimo_offset <= 1000:
            self.__primer_offset = 0

    def _calcular_bytes(self):
        """Calcula el número recomendado de bytes a rellenar.

        Para hacerlo, se basa en el número de offsets que presenta 
        el archivo.
        """
        total_ceros = len(str(self.__ultimo_offset + 1)) - 2
        bytes = "".join(("1", "".zfill(total_ceros)))
        self.configurar_bytes(int(bytes))

    # GETTERS
    def obtener_offsets(self):
        """Devuelve la lista de offsets."""
        return self.__offsets

    def obtener_primer_offset(self):
        """Devuelve el primer offset."""
        return self.__primer_offset

    def obtener_ultimo_offset(self):
        """Devuelve el último offset."""
        return self.__ultimo_offset

    def obtener_bytes(self):
        """Devuelve el número de bytes a rellenar."""
        return self.__bytes

    def obtener_relleno(self):
        """Devuelve el valor del byte de relleno."""
        return self.__relleno

    # SETTERS
    def configurar_primer_offset(self, primer_offset):
        """Configura el valor del primer offset."""
        self.__primer_offset = self._validar_offset(primer_offset)

    def configurar_ultimo_offset(self, ultimo_offset):
        """Configura el valor del último offset."""
        self.__ultimo_offset = self._validar_offset(ultimo_offset)

    def configurar_bytes(self, bytes):
        """Configura el número de bytes a rellenar."""
        self.__bytes = self._validar_bytes(bytes)

    def configurar_relleno(self, relleno=None):
        """Configura el valor del byte de relleno.

        Argumentos:
        relleno -- por defecto, aleatorio (None). 
        """
        if not relleno:
            relleno = randint(0, 255)
        self.__relleno = self._validar_relleno(relleno)

    # VALIDADORES
    def _validar_archivo(self, archivo):
        """Certifica que el archivo sea válido y tenga permisos de lectura."""
        try:
            with open(archivo, "rb") as f:
                return archivo
        except IOError as e:
            if e.errno == 2:
                raise IOError("no existe el archivo o directorio")
            elif e.errno == 13:
                raise IOError("permiso denegado para leer el archivo")
            else:
                raise IOError(e)

    def _validar_offset(self, offset):
        """Certifica que el valor del offset sea válido.

        Sólo se admiten valores mayores o iguales al primer offset
        y menores o iguales al último offset.
        """
        try:
            if self.__primer_offset <= int(offset) <= self.__ultimo_offset:
                return int(offset)
            else:
                raise ValueError
        except ValueError:
            error = "offset no válido"
            raise ValueError(error)

    def _validar_bytes(self, bytes):
        """Certifica que el número de bytes a rellenar sea válido.

        Sólo se admiten números enteros mayores o iguales a cero y
        menores o iguales al total de bytes del archivo.
        """
        try:
            if 0 <= int(bytes) <= self.__ultimo_offset:
                return int(bytes)
            else:
                raise ValueError
        except ValueError:
            error = "número de bytes a rellenar no válido"
            raise ValueError(error)

    def _validar_relleno(self, relleno):
        """Certifica que el byte de relleno sea válido.

        Sólo se admiten los siguientes valores hexadecimales: 0x00 a 0xff.
        """
        try:
            # convertimos a número
            if type(relleno) == int:
                relleno = int(relleno)
            elif type(relleno) == str:
                relleno = int(relleno, 16)
            else:
                raise TypeError

            # verificamos que se encuentre entre 0x00 y 0xff
            if 0x00 <= relleno <= 0xff:
                return hex(relleno)[2:].zfill(2).decode("hex")
            else:
                raise ValueError
        except (ValueError, TypeError):
            error = "byte de relleno no válido"
            raise Exception(error)