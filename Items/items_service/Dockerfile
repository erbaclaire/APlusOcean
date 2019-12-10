FROM django

ADD . /items_service

WORKDIR /items_service

RUN pip3 install -r requirements.txt

RUN pip install requests

RUN pip install schedule

RUN pip install python-dateutil

RUN apt-get update

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080"]
