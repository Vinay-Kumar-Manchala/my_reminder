FROM python:3.8-slim
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN apt-get update && apt-get install -y cron
RUN service cron start
COPY . /app
WORKDIR /app
EXPOSE 8989
CMD [ "python","manage.py","runserver","0.0.0.0:8989" ]