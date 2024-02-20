FROM python:3.9
WORKDIR /app
RUN apt-get update && \
    apt-get install -y sqlite3
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "api.py"]
