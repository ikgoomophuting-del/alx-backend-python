FROM python:3.10
FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app
# Install dependencies
COPY messaging_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django app
COPY messaging_app/ .

# Expose port 8000
EXPOSE 8000

# Run Django server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# Use official Python base image
chore: add Dockerfile for messaging_app containerization
docker build -t messaging_app_image .

docker run -d -p 8000:8000 --name messaging_app_container messaging_app_image









