FROM python:3.13
LABEL authors="DENIS DRUGAKOV"

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose port 8000 for Django
EXPOSE 8000

# Command to start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
