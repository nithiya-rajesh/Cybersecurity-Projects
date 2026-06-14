# Use a lightweight Python image
FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
RUN pip install flask

# Copy the server code into the container
COPY server.py .

# Create a directory for logs
RUN mkdir /logs

# Expose the port
EXPOSE 5000

# Run the server
CMD ["python", "server.py"]