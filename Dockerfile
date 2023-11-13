FROM python:3-alpine

WORKDIR /app
RUN apk update
RUN apk add bash wget alpine-sdk \
    libffi-dev openssl-dev gcc \
    g++ libmagic jpeg-dev zlib-dev
 
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3","main.py"]
