FROM python:3.9-alpine
EXPOSE 5000
ENV APP_HOME=/app
WORKDIR $APP_HOME

RUN pip install -U pipenv==2020.8.13
COPY Pipfile* ./

RUN apk add --update --no-cache --virtual .build-deps \
    && apk add --update --no-cache \
         tzdata \
         git \
         vim \
    && ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
    && mkdir -p /var/logs \
    && pipenv install --system --deploy \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*

COPY . .

CMD ["./entry.sh"]
