FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --target=/app/packages

COPY . .

FROM gcr.io/distroless/python3

WORKDIR /app

COPY --from=builder /app /app

EXPOSE 8080

ENV PYTHONPATH=/app/packages

CMD ["app.py"]

