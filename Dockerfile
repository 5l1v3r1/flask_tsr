FROM alpine

MAINTAINER Foo-Manroot


ADD /src /TSR_GP5
ADD /requirements.txt /requirements.txt

# Update
RUN apk add --update python3 py3-pip

# Install app dependencies
RUN pip3 install -U -r /requirements.txt

# Bundle app source
#COPY simpleapp.py /src/simpleapp.py

EXPOSE  8000
WORKDIR /TSR_GP5

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
