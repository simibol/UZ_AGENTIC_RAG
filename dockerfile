# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application files
COPY . .

# Expose the application port
EXPOSE 80

# Ensure gunicorn is installed
RUN pip install gunicorn

# Ensure the entrypoint is set correctly and executable
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]