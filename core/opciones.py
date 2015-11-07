#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Opciones(object):
    def __init__(self):
        self.__vaciar_directorio = None
        self.__relleno_aleatorio = None

    # SETTERS
    def configurar_vaciar_directorio(self, opcion):
        self.__vaciar_directorio = bool(opcion)

    def configurar_relleno_aleatorio(self, opcion):
        self.__relleno_aleatorio = bool(opcion)

    # GETTERS
    def obtener_vaciar_directorio(self):
        return self.__vaciar_directorio

    def obtener_relleno_aleatorio(self):
        return self.__relleno_aleatorio