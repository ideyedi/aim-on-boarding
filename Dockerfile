FROM python:3.8

MAINTAINER enrique "enrique@aimmo.co.kr"

RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    libspatialindex-dev \
    libusb-1.0-0-dev

RUN pip install --upgrade setuptools pip
RUN pip install gunicorn[gevent]
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.4.2 python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /aim-on-boarding
COPY pyproject.toml /aim-on-boarding/pyproject.toml
COPY poetry.lock /aim-on-boarding/poetry.lock
RUN poetry config virtualenvs.create false

RUN poetry install

COPY . /aim-on-boarding/

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONPATH=/aim-on-boarding

EXPOSE 8080
