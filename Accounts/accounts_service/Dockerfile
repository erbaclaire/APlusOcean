FROM django

RUN mkdir /accounts_service
WORKDIR /accounts_service
COPY . /accounts_service

WORKDIR /accounts_service

RUN pip3 install -r requirements.txt

RUN pip3 install requests

RUN apt-get update

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8083"]
