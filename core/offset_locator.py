#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from opciones import Opciones
from offsetter import OffSetter
from metodos.avfucker import AVFucker
from metodos.dsplit import DSplit
from metodos.acorralador import Acorralador


class OffsetLocator(object):
    def __init__(self, args):
        self.__archivo = args.archivo
        self.__directorio = args.directorio
        self.__metodo = args.metodo
        self.__data = None

        # opciones
        self.__vaciar_directorio = args.vaciar_directorio
        self.__relleno_aleatorio = args.relleno_aleatorio

    def ejecutar(self):
        """Inicia el procesamiento del archivo."""
        # analizamos archivo y configuramos los datos
        print "\n [*] Analizando archivo: {}".format(self.__archivo)
        self._analizar_archivo()

        # setteamos opciones
        self.__opciones = Opciones()
        self.__opciones.configurar_vaciar_directorio(self.__vaciar_directorio)
        self.__opciones.configurar_relleno_aleatorio(self.__relleno_aleatorio)

        # iniciamos menú
        self._menu()

    def _analizar_archivo(self, archivo=None):
        """Analiza archivo y configura los datos."""
        archivo = archivo if archivo else self.__archivo
        try:
            self.__data = OffSetter(archivo)
            self.__archivo = archivo
            if self.__relleno_aleatorio:
                self.__data.configurar_relleno()
        except IOError as e:
            critico = False if self.__data else True
            self._error(e, critico)

    def _analizar_directorio(self):
        """Verifica existencia del directorio."""
        try:
            if not os.path.exists(self.__directorio):
                os.makedirs(self.__directorio)
        except Exception as e:
            self._error(e, True)


    ##################
    # MENÚ PRINCIPAL #
    ##################

    def _menu(self):
        salir = False

        while not salir:
            self._imprimir_menu("principal")
            opcion = self._obtener_opcion()

            if opcion == "1":
                # llamamos al método seleccionado por el usuario
                if self.__metodo == "avfucker":
                    self._avfucker()
                elif self.__metodo == "dsplit":
                    self._dsplit()
                elif self.__metodo == "acorralador":
                    self._acorralador()
                else:   # para otros métodos
                    pass
            elif opcion == "2":
                # iniciamos menu de configuración
                self._configuracion()
            elif opcion == "99":
                salir = True
            else:
                self._error("Opción inválida", False)

        self._salir("\n [+] Saliendo")


    #################
    # CONFIGURACIÓN #
    #################

    def _configuracion(self):
        """Menú de configuración del usuario."""
        configurar = True        

        while configurar:
            try:
                self._imprimir_menu("configuracion")
                opcion = self._obtener_opcion()

                if opcion == "1":
                    primer_offset = self._preguntar("Primer offset")
                    self.__data.configurar_primer_offset(primer_offset)

                elif opcion == "2":
                    ultimo_offset = self._preguntar("Último offset")
                    self.__data.configurar_ultimo_offset(ultimo_offset)

                elif opcion == "3":
                    bytes = self._preguntar("Número de bytes a modificar")
                    self.__data.configurar_bytes(bytes)

                elif opcion == "4":
                    adicional = "(enter para byte aleatorio)"
                    relleno = self._preguntar("Byte de relleno", adicional)
                    if relleno == "":
                        relleno == None
                    self.__data.configurar_relleno(relleno)

                elif opcion == "5":
                    opcion = self._preguntar("Vaciar directorio", "(s/n)")

                    if opcion.lower() == "s":
                        self.__opciones.configurar_vaciar_directorio(True)

                    elif opcion.lower() == "n":
                        self.__opciones.configurar_vaciar_directorio(False)

                    else:
                        raise Exception("Opción inválida")

                elif opcion == "6":
                    directorio = self._preguntar("Directorio")
                    if directorio:
                        self.__directorio = directorio

                elif opcion == "7":
                    archivo = self._preguntar("Archivo")
                    self._analizar_archivo(archivo)

                elif opcion == "8":
                    # cambiamos método
                    self._cambiar_metodo()

                elif opcion == "99":
                    configurar = False

                else:
                    raise Exception("Opción inválida")

            except Exception as e:
                self._error(e, False)

    def _obtener_configuracion(self):
        """Obtiene la configuración de los datos."""
        self.__primer_offset = self.__data.obtener_primer_offset()
        self.__ultimo_offset = self.__data.obtener_ultimo_offset()
        self.__bytes = self.__data.obtener_bytes()
        self.__relleno = self.__data.obtener_relleno()

        self.__vaciar_directorio = self.__opciones.obtener_vaciar_directorio()


    ##################
    # CAMBIAR MÉTODO #
    ##################

    def _cambiar_metodo(self):
        cambiar_metodo = True

        while cambiar_metodo:
            self._imprimir_menu("cambiar metodo")
            opcion = self._obtener_opcion()

            if opcion == "1":
                self.__metodo = "avfucker"
                cambiar_metodo = False
            elif opcion == "2":
                self.__metodo = "dsplit"
                cambiar_metodo = False
            elif opcion == "3":
                self.__metodo == "acorralador"
                cambiar_metodo = False
            else:
                self._error("Opción inválida", False)


    ###########
    # MÉTODOS #
    ###########

    def _avfucker(self):
        """Ejecuta el método avfucker."""
        print "\n [*] Ejecutando AVFucker"
        
        print " [*] Analizando directorio: {}".format(self.__directorio)
        self._analizar_directorio()

        try:
            avfucker = AVFucker(self.__archivo,
                self.__data,
                self.__opciones,
                self.__directorio)
            avfucker.ejecutar()

            self._analizar_archivos_creados()

        except Exception as e:
            self._error(e, True)

    def _dsplit(self):
        """Ejecuta el método dsplit."""
        print "\n [*] Ejecutando DSplit"

        print " [*] Analizando directorio: {}".format(self.__directorio)
        self._analizar_directorio()

        try:
            dsplit = DSplit(self.__archivo,
                self.__data,
                self.__opciones,
                self.__directorio)
            dsplit.ejecutar()

            self._analizar_archivos_creados()

        except Exception as e:
            self._error(e, True)

    def _acorralador(self):
        """Ejecuta el método acorralador."""
        print "\n [*] Ejecutando el acorralador de firmas."
        try:
            acorralador = Acorralador(self.__archivo,
                self.__data,
                self.__opciones)
            acorralador.ejecutar()
            self._informar("OK")
        except Exception, e:
            self._error(e, True)

    def _analizar_archivos_creados(self):
        """Analiza los archivos creados."""
        archivos_creados = self._obtener_archivos_creados()
        self._informar("OK (analice los archivos y presione enter para continuar)")
        self.__archivos_limpios = self._obtener_archivos_creados()

        if not self.__archivos_limpios:
            self._informar("Se han detectado todos los archivos", "-")

        elif self.__archivos_limpios == archivos_creados:
            self._informar("Todos los archivos son indetectables")

        else:
            seleccionar_offsets = True
            
            while seleccionar_offsets:
                try:
                    self._imprimir_menu("seleccionar offsets")
                    opcion = self._obtener_opcion()
                    
                    # configuramos primer y último offset
                    grupo = int(opcion) - 1
                    offsets = self.__archivos_limpios[grupo]
                    self.__data.configurar_primer_offset(offsets[0])
                    self.__data.configurar_ultimo_offset(offsets[1])
                    
                    # configuramos el número de bytes
                    bytes = (int(self.__bytes) / 10) if self.__bytes >= 10 else 1
                    self.__bytes = self.__data.configurar_bytes(bytes)

                    # finalizamos el bucle
                    seleccionar_offsets = False
                except Exception as e:
                    self._error("Opción inválida: ", False)

    def _obtener_archivos_creados(self):
        """Obtiene los archivos creados luego de ejecutar un método."""
        obtener_offset = lambda x:int(x[:x.index("_")])

        # obtenemos la lista de archivos y la ordenamos
        archivos = os.listdir(self.__directorio)
        try:
            archivos = sorted(archivos, key=obtener_offset)
        except Exception as e:
            self._error("manipulación de archivos", True)

        inicio = self.__primer_offset
        fin = self.__ultimo_offset
        
        grupos = []
        grupo = []

        for archivo in archivos:
            offset = obtener_offset(archivo)
            while inicio <= fin:
                if inicio == offset:
                    grupo.append(offset)
                    inicio += self.__bytes
                    break
                if grupo:
                    grupos.append(grupo)
                grupo = []
                inicio += self.__bytes
        if grupo:
            grupos.append(grupo)

        for i in range(len(grupos)):
            grupo = grupos[i]
            primer_offset = grupo[0]
            ultimo_offset = grupo[-1] if (len(grupo) > 1) else grupo[0]
            if (ultimo_offset + self.__bytes) <= self.__ultimo_offset:
                ultimo_offset += self.__bytes
            grupos[i] = [primer_offset, ultimo_offset]

        return grupos


    ############################
    # Interfaz de comunicación #
    ############################

    def _imprimir_configuracion(self):
        """Imprime la configuración de los datos."""
        self._obtener_configuracion()

        print "\n [*] Configuración actual:"
        print "\t- Método: {}".format(self.__metodo)

        print "\n\t- Archivo: {}".format(self.__archivo)
        print "\t- Directorio: {}".format(self.__directorio)

        print "\n\t- Primer offset: {}".format(self.__primer_offset)
        print "\t- Último offset: {}".format(self.__ultimo_offset)
        print "\t- Bytes a modificar: {}".format(self.__bytes)
        relleno = hex(int(self.__relleno.encode("hex"), 16))
        print "\t- Byte de relleno: {}".format(relleno)
        vaciar_directorio = "sí" if self.__vaciar_directorio else "no"
        print "\t- Vaciar directorio: {}".format(vaciar_directorio)

    def _imprimir_menu(self, menu):
        """Imprime menú de usuario."""
        self._limpiar()

        # imprimimos configuración actual
        self._imprimir_configuracion()

        # imprimimos menu
        if menu == "principal":
            menu  = "\n [MENU] Seleccione una opción:"
            menu += "\n\t1) Ejecutar"
            menu += "\n\t2) Configuración"
            menu += "\n\t99) Salir"

        elif menu == "configuracion":
            menu  = "\n [CONFIGURACIÓN] Seleccione una opción:"
            menu += "\n\t1) Primer offset"
            menu += "\n\t2) Último offset"
            menu += "\n\t3) Número de bytes a modificar"
            menu += "\n\t4) Byte de relleno"
            menu += "\n\t5) Vaciar directorio"
            menu += "\n\t6) Cambiar directorio"
            menu += "\n\t7) Cambiar archivo"
            menu += "\n\t8) Cambiar método"
            menu += "\n\t99) Salir"

        elif menu == "cambiar metodo":
            menu  = "\n [CAMBIAR MÉTODO] Seleccione una opción:"
            menu += "\n\t1) AVFucker"
            menu += "\n\t2) DSplit"
            menu += "\n\t3) Acorralador de firmas"

        elif menu == "seleccionar offsets":
            menu = "\n [SELECCIONAR OFFSETS] Seleccione una opción:"
            i = 0

            for grupo in self.__archivos_limpios:
                i += 1
                menu += "\n\t{0}) {1} : {2}".format(i, grupo[0], grupo[1])

        print menu

    def _limpiar(self):
        """Limpia la pantalla."""
        cmd = "cls" if os.name == "nt" else "clear"
        os.system(cmd)

    def _obtener_opcion(self):
        return raw_input(" >>> ")

    def _preguntar(self, pregunta, adicional=""):
        """Interfaz para realizar preguntas."""
        return raw_input("\n [?] ¿{}? {}: ".format(pregunta, adicional))

    def _error(self, error, critico):
        msj = "\n [!] Error: {}.".format(error)
        if critico:
            self._salir(msj)
        raw_input(msj)

    def _informar(self, msj, signo="+"):
        raw_input(" [{}] {}".format(signo, msj))

    def _salir(self, msj):
        sys.exit(msj)