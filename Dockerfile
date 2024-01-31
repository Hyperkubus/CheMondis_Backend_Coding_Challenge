FROM python:latest

ENV PYTHONUNBUFFERED 1

COPY src/weatherApi /weatherApi

# Install any needed packages specified in requirements.txt
WORKDIR /weatherApi

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000