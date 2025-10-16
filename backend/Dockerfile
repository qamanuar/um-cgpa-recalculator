# Start with a lean official Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file first for faster rebuilds
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Define the command to run your app when the container starts
CMD uvicorn main:app --host 0.0.0.0 --port $PORT