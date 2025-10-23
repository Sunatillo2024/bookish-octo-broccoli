# Base image
FROM python:3.11-slim

# Ishchi papka
WORKDIR /app

# requirements ni copy va install qilamiz
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# App fayllarini copy qilamiz
COPY . .

# Default command (FastAPI uchun)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
