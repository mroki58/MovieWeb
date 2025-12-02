FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl

RUN pip install uv

COPY . .

RUN uv sync --frozen --no-install-project

EXPOSE 5000

CMD ["uv", "run", "python", "-m", "flask", "run"]