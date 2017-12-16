FROM ubuntu:xenial

MAINTAINER Foo-Manroot


ADD /src /TSR_GP5
ADD /requirements.txt /requirements.txt

# Actualiza y instala las dependencias (MongoDB)
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3 python3-pip mongodb-server

# Instala las dependencias de Python
RUN pip3 install -U -r /requirements.txt

# Expone el puerto y ejecuta 'main.py'
EXPOSE  8000
WORKDIR /TSR_GP5

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
