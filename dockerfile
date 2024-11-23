# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/
# RUN python manage.py make migrations

# Expose the port the app will run on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]