# Use Python base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies (ignore SSL verification for now)
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt

# Expose Flask default port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
