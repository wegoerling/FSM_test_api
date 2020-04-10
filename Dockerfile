FROM ubuntu:16.04

MAINTAINER Walter Goerling "11wgoerling@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    set $FLASK_APP=app.py && \
    set $FLASK_ENV=development

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "flask", "run" ]