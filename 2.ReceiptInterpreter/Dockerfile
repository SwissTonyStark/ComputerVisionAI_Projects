# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install system dependencies for Whisper and FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app will run on
EXPOSE 5000

# Command to run the server
CMD ["python", "scripts/server.py"]
