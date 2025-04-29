# Using the official python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt
COPY requirements.txt .

# Setting up dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into a container
COPY . .

# Set the environment variable for proper importing
ENV PYTHONPATH=/app

# Application start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

