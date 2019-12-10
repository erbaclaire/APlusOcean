FROM python:3

ADD . /auctions_service

WORKDIR /auctions_service

RUN pip3 install -r requirements.txt

RUN pip3 install requests

RUN apt-get update

CMD ["mongod"]

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8084"]
