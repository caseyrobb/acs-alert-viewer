FROM registry.access.redhat.com/ubi9/ubi-minimal

MAINTAINER Casey Robb "casey.robb@redhat.com"

RUN microdnf update -y && microdnf install python3-pip -y && microdnf clean all -y

COPY ./requirements.txt /app/requirements.txt
COPY ./templates /app
COPY ./start.sh /app

WORKDIR /app

RUN python3 -m pip install -r requirements.txt
RUN chmod +x start.sh

COPY . /app

EXPOSE 5000

USER 1001

CMD ["python3", "app.py"]