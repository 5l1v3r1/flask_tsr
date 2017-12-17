#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####
# Módulos propios
####

from scraper import Scraper

####
# Bibliotecas externas
####

import flask
import time \
    , logging

# Para ejecutar las tareas en segundo plano
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


###
# VARIABLES GLOBALES y cosas varias
###
logging.basicConfig (level = logging.INFO)

logging.getLogger (__name__).info ("\n\t => Iniciando servidor...\n")



app = flask.Flask (__name__)
planificador = BackgroundScheduler ()
scraper = Scraper (max_elems = 10)

###########################

####
# MÉTODOS EXPUESTOS (ENDPOINTS)
####

@app.route ("/umbral", methods = ["POST"])
def cambiar_umbral ():

    if not flask.request.form ['umbral']:
        return "404, m8"

    return flask.render_template ("index.html"
                                , nums = scraper.nums
                                , umbral = float (flask.request.form ["umbral"])
    )



@app.route ("/")
def index ():
    return flask.render_template ("index.html"
                                , nums = scraper.nums
    )




####
# MAIN
####


if __name__ == '__main__':

    logger = logging.getLogger (name = __name__)

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
