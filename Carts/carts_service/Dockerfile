FROM django

ADD . /carts_service

WORKDIR /carts_service

RUN pip3 install -r requirements.txt

RUN pip install requests

RUN pip install schedule

RUN apt-get update

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8082"]
