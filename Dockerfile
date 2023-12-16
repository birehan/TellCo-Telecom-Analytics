# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install build dependencies
RUN apt-get update \
    && apt-get install -y gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "your_main_script.py"]

# # Run streamlit when the container launches
# CMD ["streamlit", "run", "/app/dashboard/dashboard.py"]