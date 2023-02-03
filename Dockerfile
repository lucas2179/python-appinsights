# Use a lightweight Python image as the base
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev

# Install the required packages
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Set the environment variable for the Application Insights instrumentation key
ENV APP_INSIGHTS_INSTRUMENTATION_KEY <your_instrumentation_key>

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]