#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####
# Módulos propios
####

from scraper import Scraper

####
# Bibliotecas externas
####

from flask import Flask
import time \
    , logging

# Para ejecutar las tareas en segundo plano
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


###
# VARIABLES GLOBALES
###

app = Flask (__name__)
planificador = BackgroundScheduler ()
scraper = Scraper (max_elems = 3)

###########################

####
# MÉTODOS EXPUESTOS (ENDPOINTS)
####

@app.route ("/")
def index ():
    return str (scraper.nums)




####
# MAIN
####


if __name__ == '__main__':


    logging.basicConfig (level = logging.INFO)

    logger = logging.getLogger (name = __name__)

    logger.info ("\n\t => Iniciando servidor...\n")

    # Establece los parámetros para ejecutar las tareas en segundo plano
    planificador.start ()

    # Ejecuta scraper.actualizar_datos
    planificador.add_job (
        func = scraper.actualizar_datos
        , trigger = IntervalTrigger (seconds = 10)
        , id = "actualizar_datos"
        , name = "Actualización de los datos cada dos minutos"
        , replace_existing = True
    )

    app.run (host = "0.0.0.0", port = 8000)

    logger.info ("\n\t => Terminando tareas en segundo plano...\n")
    planificador.shutdown (wait = True)
    logger.info ("\n\t => Listo\n")
