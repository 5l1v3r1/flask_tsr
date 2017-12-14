#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import beebotte \
    , json

class Manejador ():
    """
    Clase para trabajar con Beebotte
    """

    def __init__ (self):
        """
        Constructor
        """

        # Carga las claves del fichero API.keys y crea el cliente con ellas
        with open ("API.keys") as f:
            keys = json.load (f)

        self.client = beebotte.BBT ( keys ["api"], keys ["secret"] )



    def escribir_datos (self):
        """
        Escribe los datos en el recurso 'nums' del módulo 'tsr'
        """

        res = beebotte.

        pass
