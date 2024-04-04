# syntax = docker/dockerfile:1.2
FROM python:3.12

WORKDIR /bestpriceapi

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY app.py db_adapters.py services.py ./

# RUN --mount=type=secret,id=env,target=/var/secrets/env cat /var/secrets/env  


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8085"]