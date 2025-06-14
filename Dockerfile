FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir mangaba openai
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
