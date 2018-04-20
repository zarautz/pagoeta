FROM python:3.6-alpine3.7

# ensure Alpine Linux includes the packages necessary for `lxml`
RUN apk add --no-cache build-base \
    py-lxml libxml2-dev libxslt-dev

# install app
RUN mkdir /app
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --deploy --system
COPY . /app

CMD gunicorn pagoeta:app
