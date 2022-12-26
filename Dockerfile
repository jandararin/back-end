FROM python:3.9.6
RUN apt-get update -y
COPY ./src /var/app/back-end/src
COPY ./requirements.txt /var/app/back-end/requirements.txt
RUN pip install -r /var/app/back-end/requirements.txt
WORKDIR /var/app/back-end
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080", "--app-dir", "./src"]
