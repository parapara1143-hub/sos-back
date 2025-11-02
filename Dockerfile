FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=manage.py
CMD ["gunicorn","-k","eventlet","-w","1","-b","0.0.0.0:8000","manage:app"]
