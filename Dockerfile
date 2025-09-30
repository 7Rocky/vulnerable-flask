FROM python:3.12-alpine

RUN apk add --no-cache --update supervisor
RUN python -m pip install --upgrade pip

WORKDIR /app
COPY requirements.txt /app/
COPY supervisord.conf /etc/supervisord.conf

RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY src /app/
EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
