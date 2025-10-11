FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

chore: add Dockerfile for messaging_app containerization
docker build -t messaging_app_image .

docker run -d -p 8000:8000 --name messaging_app_container messaging_app_image

