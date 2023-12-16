# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the dashboard folder into the container at /app
COPY dashboard /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the port that Streamlit will run on
EXPOSE 8501

# Define environment variable
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Run streamlit when the container launches
CMD ["streamlit", "run", "/app/dashboard/dashboard.py"]
