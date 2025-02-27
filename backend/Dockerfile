# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the httpx binary
RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/projectdiscovery/httpx/releases/download/v1.6.10/httpx_1.6.10_linux_amd64.zip \
    && apt-get install -y unzip \
    && unzip httpx_1.6.10_linux_amd64.zip -d /usr/local/bin/ \
    && rm httpx_1.6.10_linux_amd64.zip

# Copy the rest of your application code
COPY ./app .

# Expose the port your FastAPI app runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
