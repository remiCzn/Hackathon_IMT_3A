FROM debian:latest
WORKDIR /app
COPY requirements.txt /app
RUN apt update && apt upgrade
RUN apt install -y python3-pip python3 libmariadb-dev
RUN pip install -r requirements.txt
ADD . /app/
CMD ["python3","-u","index.py"]
