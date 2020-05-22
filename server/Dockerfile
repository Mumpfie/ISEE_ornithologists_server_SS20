FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN python -m pip --no-cache-dir install aiofiles python-multipart sqlalchemy psycopg2 && mkdir /pictures

COPY . /app