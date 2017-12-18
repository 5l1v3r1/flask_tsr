#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####
# Módulos propios
####
import db   \
    , bbdd_iot


####
# Bibliotecas externas
####

import urllib3  \
    , re        \
    , logging

from random import random
from time import time
from bs4 import BeautifulSoup

class Scraper ():
    """
    Clase con los métodos necesarios para obtener los datos pedidos para la práctica
    desde
        http://www.numeroalazar.com.ar/
    """

    def __init__ (self, max_elems = 100):
        """
        Constructor

        Args:
            max_elems (opcional) -> Número máximo de elementos en la lista. Si no se
                especifica, por defecto es 100
        """
        self.url = "http://www.numeroalazar.com.ar/"

        self.max_elems = max_elems

        self.manejador_bbdd_iot = bbdd_iot.Manejador ()
        self.manejador_db = db.Manejador ()

        # Inicializa los elementos con lo guardado en las bases de datos
        self.nums = self.leer_bbdd ()


    def leer_bbdd (self, umbral = None, max_elems = None):
        """
        Obtiene de las bases de datos todos los números, hasta un máximo de
        self.max_elems

        Args:
            umbral (opcional) -> Límite superior para filtrar

        Returns:
            Un diccionario con todos los datos obtenidos
        """
        datos = {}

        if not max_elems:
            max_elems = self.max_elems


        # Primero lee la bbdd local, y luego Beebotte
        for d in self.manejador_db.leer_datos ():
            # Esto debería devolver diccionarios
            if type (d) == dict:
                for k in d:
                    if (len (datos) < max_elems
                        and
                        k not in datos
                    ):
                        if umbral:
                            if d [k] >= umbral:
                                datos [k] = d [k]
                        else:
                            datos [k] = d [k]

        for elem in self.manejador_bbdd_iot.leer (limit = self.max_elems):
            d = elem ['data']
            # De nuevo, debería devolver diccionarios
            if type (d) == dict:
                for k in d:
                    if (len (datos) < max_elems
                        and
                        k not in datos
                    ):
                        if umbral:
                            if d [k] >= umbral:
                                datos [k] = d [k]
                        else:
                            datos [k] = d [k]

        if len (datos) > 0:
            logging.getLogger (__name__).info (
                "\n\t => Datos recuperados de las BBDD: {}".format (datos)
            )

        return datos


    def actualizar_datos (self):
        """
        Realiza las peticiones y el procesamiento necesario para obtener los datos
        """
        http = urllib3.PoolManager ()
        req = http.request ("GET", self.url)

        if req.status != 200:
            # Petición rechazada
            return
        else:
            html = req.data

        parsed = BeautifulSoup (html, "html.parser")
        # Obtiene el elemento con los números generados
        nums_div = parsed.find_all ("div", {"id": "numeros_generados"}) [0]

        # Patrón para un número decimal
        pattern = re.compile (r"^\d+([.]\d+)?$")

        # Añade los números a la lista
        for elem in nums_div.strings:

            # Comprueba que sea un número (para eliminar el texto del título)
            if (pattern.match (elem)):

                longitud = len (self.nums)
                # Si hay más elementos que los máximos,
                # borra uno aleatorio (para mantener el límite)
                if longitud >= self.max_elems:
                    self.nums.pop (
                        list (self.nums) [
                                    int ( (random () * longitud) % longitud)
                        ]
                    )

                self.guardar_dato (elem)
                # Sólo obtiene el primer número (eso dice en el enunciado...)
                break


    def guardar_dato (self, num):
        """
        Guarda el dato especificado en las bases de datos, añadiendo la estampa de
        tiempo (tal y como se especifica en el enunciado)

        Args:
            num -> Número a guardar en la base de datos
        """
        timestamp = int (time ())
        self.nums [ str (timestamp) ] = float (num)

        # Guarda los datos en las BBDD
        self.manejador_db.guardar_dato (
            {
                str (timestamp): float (num)
            }
        )

        self.manejador_bbdd_iot.escribir (
            {
                str (timestamp): float (num)
            }
        )

        logging.getLogger (__name__).info (
            "\n\t => Añadido número a las base de datos: {}\n".format (num)
        )



    def calc_media (self):

        acc = 0.
        n = 0.

        # Primero lee la bbdd local, y luego Beebotte
        for d in self.manejador_db.leer_datos ():
            # Esto debería devolver diccionarios
            if type (d) == dict:
                for k in d:
                    acc += d [k]
                    n += 1


        for elem in self.manejador_bbdd_iot.leer (limit = self.max_elems):
            d = elem ['data']
            # De nuevo, debería devolver diccionarios
            if type (d) == dict:
                for k in d:
                    acc += d [k]
                    n += 1

        return acc / n
