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



    def escribir (self, datos):
        """
        Escribe los datos proporcionados en el recurso 'nums' del módulo 'tsr'

        Args:
            datos -> Objeto a escribir
        """
        self.client.write ("tsr", "nums", datos)

        print ("Datos escritos: {}".format (datos))


    def leer (self, limit = 3):
        """
        Lee los datos del recurso 'nums' del módulo 'tsr'

        Args:
            limit (opcional) -> Número máximo de elementos a devolver
        """
        elems = self.client.read ("tsr", "nums", limit = limit)

        return elems
