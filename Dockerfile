FROM python:alpine

WORKDIR /root

COPY . .

RUN apk add --no-cache gcc musl-dev \
    && pip install -r requirements.txt --extra-index-url https://alpine-wheels.github.io/index \
    && pip install 'uvicorn[standard]'

RUN rm -rf /tmp/* /var/cache/apk/*

ENTRYPOINT [ "uvicorn", "server:app", "--host", "0.0.0.0" ]