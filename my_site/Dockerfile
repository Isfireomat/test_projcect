FROM python:3.11.8

SHELL ["/bin/bash","-c"]

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install --upgrade pip
RUN pip install poetry
RUN apt update

RUN useradd -rms /bin/bash project 
RUN chmod 777 /opt /run

WORKDIR /project
COPY poetry.lock pyproject.toml /project/
RUN poetry install
RUN mkdir /project/static
RUN chown -R project:project /project 
RUN chmod 755 /project

COPY . .


CMD ["gunicorn", "test_site.wsgi:application", "-c", "gunicorn_conf.py"]    