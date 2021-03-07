FROM alpine:edge

WORKDIR /app

RUN apk update

RUN apk add build-base py3-pip python3-dev \
    gcc

COPY . .

RUN pip3 install -U -r requirements.txt

CMD ["python3", "main.py"]
