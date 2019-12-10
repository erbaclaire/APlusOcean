FROM django

ADD . /frontend

WORKDIR /frontend

RUN pip3 install -r requirements.txt

RUN apt-get update

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]

