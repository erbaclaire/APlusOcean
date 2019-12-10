FROM django

ADD . /notifications_service

WORKDIR /notifications_service

RUN pip3 install -r requirements.txt

RUN pip install requests

RUN apt-get update

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8081"]
