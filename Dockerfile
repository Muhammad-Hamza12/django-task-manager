FROM python:3.9-slim

# Install system dependencies including ODBC driver
RUN apt-get update && \
    apt-get install -y \
    unixodbc \
    unixodbc-dev \
    gnupg2 \
    curl && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install Python dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . /app/

# Set the entrypoint
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
