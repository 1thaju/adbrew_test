FROM python:3.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/src \
    ENV_TYPE=staging \
    MONGO_HOST=mongo \
    MONGO_PORT=27017

WORKDIR /src

COPY src/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir "pip<24.1" \
    && sed '/^uWSGI==/d' /tmp/requirements.txt > /tmp/requirements-container.txt \
    && pip install --no-cache-dir -r /tmp/requirements-container.txt

COPY src /src

EXPOSE 8000
CMD ["python", "rest/manage.py", "runserver", "0.0.0.0:8000"]
