# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install colorama

# Copy the analyzer code
COPY log_analyzer.py .

# Run the analyzer (using python -u for unbuffered output so logs show up instantly)
CMD ["python", "-u", "log_analyzer.py"]