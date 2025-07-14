FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD 'admin'

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install django && \
    pip install djbackup

# copy project to container
COPY . /app/

# create log file
RUN mkdir logs
RUN touch ./logs/server.log

# move to source directory
WORKDIR /app/src

# create sqlite db(manual)
RUN touch db.sqlite3

# collectstatic
RUN python manage.py collectstatic --noinput

# migrate
RUN python manage.py migrate

# create superuser
RUN python manage.py createsuperuser --noinput --username admin --email admin@example.com

EXPOSE 8000

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
