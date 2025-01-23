FROM python:3.13.1

ENV WEB_APP_DIR=/app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY src/ /app/src
COPY requirements.txt alembic.ini key.json /app
COPY docker/app/start.sh /app

RUN apt-get update
RUN apt-get install -y --no-install-recommends netcat-traditional
RUN chmod +x /app/start.sh
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

CMD ./start.sh