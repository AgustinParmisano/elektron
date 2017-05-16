FROM ubuntu:latest
MAINTAINER Agustin Parmisano "agustinparmisano@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN mkdir /opt/elektron
WORKDIR /opt/elektron
ADD requirements.txt /opt/elektron/
RUN pip install -r requirements.txt
ADD . /opt/elektron
WORKDIR /opt/elektron
ENTRYPOINT ["python"]
CMD ["app.py"]
#RUN python app.py
