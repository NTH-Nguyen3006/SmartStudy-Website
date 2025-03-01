FROM python:3.11.3-slim-bullseye

WORKDIR /app

COPY . /app/

RUN ls

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
