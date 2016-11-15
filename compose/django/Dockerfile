FROM python:3.5.2

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y libproj-dev gdal-bin python-gdal libgeoip1

RUN apt-get install supervisor -y
ADD ./compose/django/supervisord.conf /etc/supervisor.d/dc_traffic_tickets.conf
CMD ["supervisord", "-c", "/etc/supervisord.conf"]


# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install -r /requirements/production.txt \
    && groupadd -r django \
    && useradd -r -g django django

RUN pip install -e git+https://github.com/groveco/django-sql-explorer.git#egg=explorer

COPY . /app
RUN chown -R django /app

COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

WORKDIR /app

# no entry point on production settings as it messes with env files
# ENTRYPOINT ["/entrypoint.sh"]
