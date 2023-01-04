FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt /app
RUN apt install gcc
RUN pip install -r requirements.txt
ADD . /app/
CMD ["python","-u","index.py"]
