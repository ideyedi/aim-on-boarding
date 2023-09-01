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

WORKDIR /eimmo-backend
COPY pyproject.toml /eimmo-backend/pyproject.toml
COPY poetry.lock /eimmo-backend/poetry.lock
RUN poetry config virtualenvs.create false

# bluewhale private pypi
#RUN poetry config repositories.bluewhale https://pypi.bluewhale.kr
#RUN poetry config http-basic.bluewhale $PYPI_SECRET_USER $PYPI_SECRET_KEY

RUN poetry install
#RUN pip install azure-appconfiguration==1.3.0

COPY . /eimmo-backend/

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONPATH=/eimmo-backend

EXPOSE 8080
