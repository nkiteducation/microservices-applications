FROM python:3.13.5-slim

COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /bin/

WORKDIR /usr/src/

COPY pyproject.toml /usr/src/

RUN uv pip install --system .

COPY ./app /usr/src/app
COPY ./scripts /usr/src/scripts
COPY ./alembic.ini /usr/src

EXPOSE 8000

CMD ["gunicorn", "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "5", \
     "--timeout", "120"]
