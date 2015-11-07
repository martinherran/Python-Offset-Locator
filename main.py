#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

from core.offset_locator import OffsetLocator

def parser():
    help_formatter = lambda prog: argparse.HelpFormatter(prog, 
                                    max_help_position=52, 
                                    width=120)
    
    parser = argparse.ArgumentParser(
        prog="Python Offset Locator",
        formatter_class=help_formatter,
        description="Python Offset Locator",
        epilog="©2015 Herrán Martín"
        )
    
    parser.add_argument("archivo", help="archivo a analizar")

    parser.add_argument("-m", "--metodo", required=True,
        choices=set(("avfucker", "dsplit", "acorralador")),
        help="método que se aplicará al archivo seleccionado",
        )

    parser.add_argument("-d", "--directorio", dest="directorio",
        default="offsets",
        help="directorio donde se crearán los archivos resultantes",
        )

    parser.add_argument("-l", "--limpiar", action="store_true",
        dest="vaciar_directorio",
        help="borra los archivos del directorio seleccionado",
        )

    parser.add_argument("-a", "--aleatorio", action="store_true",
        dest="relleno_aleatorio",
        help="byte de relleno aleatorio",
        )
 
    parser.add_argument("--version", action="version",
        version="%(prog)s v1.0")

    return parser.parse_args()


def main():
    args = parser()

    try:
        offset_locator = OffsetLocator(args)
        offset_locator.ejecutar()
    except KeyboardInterrupt:
        sys.exit(" [!] KeyboardInterrupt")

if __name__ == "__main__":
    main()