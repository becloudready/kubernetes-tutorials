FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install requests

# Copy the interview script
COPY troubleshoot_scenarios.py .

# Create directory for ConfigMap mount
RUN mkdir -p /etc/app

# Set default command
CMD ["python", "./troubleshoot_scenarios.py"]
