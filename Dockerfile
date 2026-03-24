# Dockerfile for FastAPI Service

# Use the official Python 3.11 base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file first to utilize caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port on which the app will run
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]