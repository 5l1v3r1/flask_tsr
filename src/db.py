#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo  \
    , logging

class Manejador ():
    """
    Manejador para la base de datos local (usando MongoDB)
    """

    def __init__ (self):
        """
        Constructor
        """

        # Obtiene el cliente para la base de datos
        cliente = pymongo.MongoClient ("mongodb://127.0.0.1:27017")

        self.db_collection = cliente ["tsr"].nums



    def guardar_dato (self, datos):
        """
        Guarda el número aportado en la base de datos

        Args:
            datos -> Datos a ser guardados
        """
        resultado = self.db_collection.insert_one ( { "datos": datos } )

        logging.getLogger (__name__).info ("\n\t --> Datos guardados en MongoDB")


    def leer_datos (self):
        """
        Generador que devuelve todos los datos en la base de datos

        Returns:
            Un generador con los datos
        """
        for x in self.db_collection.find ():
            yield x ["datos"]
