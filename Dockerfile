FROM python:latest

ENV PYTHONUNBUFFERED 1

#COPY src/weatherApi /weatherApi
VOLUME /weatherApi

# Install any needed packages specified in requirements.txt
WORKDIR /weatherApi
COPY src/weatherApi/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python /weatherApi/manage.py makemigrations && python /weatherApi/manage.py migrate && python /weatherApi/manage.py compilemessages && python /weatherApi/manage.py runserver 0.0.0.0:8000