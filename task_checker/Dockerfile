FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
# Note: --trusted-host flags may be needed in restricted network environments
COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy application code
COPY src /app/src

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set Python path to include src directory
ENV PYTHONPATH=/app/src

# Expose port
EXPOSE 8000

# Run the entrypoint script
CMD ["/app/entrypoint.sh"]