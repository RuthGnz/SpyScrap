FROM python:3.7-alpine3.9
RUN apk add --update \
  && rm -rf /var/cache/apk/*
COPY requirements.txt /app/
COPY src/ /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b","0.0.0.0:5000","-t","1800","api:app","--reload"]