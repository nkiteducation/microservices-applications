FROM python:3.13.5-slim

COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /bin/

WORKDIR /usr/src/app

COPY ./pyproject.toml .
RUN uv pip install --system -r pyproject.toml

COPY ./app .

EXPOSE 8000
CMD ["gunicorn", "main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "120"]