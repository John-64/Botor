FROM python:3.11.4-alpine3.18

RUN apk update && \
    apk add --no-cache python3 python3-dev py3-pip build-base cmake

COPY . /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "botor.py" ]
