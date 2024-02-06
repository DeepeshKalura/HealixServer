# Use the official Python image as the base image
FROM python:3.11.5

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port that FastAPI will run on
EXPOSE 3100

# Command to run the FastAPI application
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", ":3100", "app.main:app"]
