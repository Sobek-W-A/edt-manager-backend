FROM python:3.12

ARG CACHEBUST=1  # Dummy build argument for cache invalidation

RUN mkdir build
WORKDIR /build

COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
EXPOSE 8000

ENV WAIT_VERSION 2.11.0
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

CMD python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4