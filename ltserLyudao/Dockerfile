FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

RUN python manage.py collectstatic --noinput
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ADD https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh /usr/wait-for-it.sh

RUN chmod +x /usr/wait-for-it.sh

EXPOSE 8200

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]