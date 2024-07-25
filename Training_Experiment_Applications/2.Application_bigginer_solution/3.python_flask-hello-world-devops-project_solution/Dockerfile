# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8585 available to the world outside this container
EXPOSE 8585

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python3", "./app.py"]
