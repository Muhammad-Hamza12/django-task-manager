# Django Task Project - README

## Overview
This project demonstrates a robust implementation of Django and Python development with a focus on APIs, custom authentication, and task scheduling. It integrates **Microsoft SQL Server (Local)** as the database backend and utilizes **Celery** for asynchronous and scheduled tasks. The project is containerized using **Docker** for seamless deployment, except for the **SQL Server**, which needs to be set up locally.

---

## Features

### 1. **Project Setup**
- Developed using **Django** with **Python 3.9**.
- Uses **Microsoft SQL Server (Local)** as the database backend.

---

### 2. **Custom Authentication and Authorization**
- Implements **JWT (JSON Web Tokens)** for secure user authentication.
- Tokens are set to expire after **5 minutes** for enhanced security.
- Protects all endpoints to ensure only authenticated users can access them.

---

### 3. **API Endpoints**
#### a. **Post API**
- Allows authenticated users to create tasks by providing a `title` and `duration`.  
- Automatically stores timestamps and associates tasks with the logged-in user.

#### b. **Get API**
- Retrieves the **last 4 tasks** created by the logged-in user using Django's filtering capabilities.

#### c. **Retrieve API**
- Fetches a specific task created by the logged-in user.  
- Uses a **raw SQL query** for implementation.

#### d. **Update API**
- Allows updating only the `title` of a task.  
- Prevents updates to the `duration` field.  
- Implemented using a **raw SQL query**.

#### e. **Delete API**
- Enables users to delete tasks they created.  
- Prevents deletion of tasks created by other users.

---

### 4. **Test Cases**
- Includes comprehensive test cases to validate all API endpoints and custom functionalities.

---

### 5. **Custom Management Command**
- Implements a Django management command to:
  - Iterate through all tasks in the database.
  - Display each task at intervals of **10 seconds** (using custom output instead of `print()`).

---

### 6. **Celery Integration**
- Integrated **Celery** with **Redis** to manage asynchronous task execution.  
- Handles background task processing efficiently.

---

### 7. **Scheduled Tasks**
- Configured **Celery Beat** to run scheduled tasks:
  - A scheduled task runs every **1 minute**, printing the `title`, `duration`, and timestamps of tasks created by the user with `id=1`.

---

### 8. **Docker Containerization**
- Fully containerized project with **Docker** for deploying the Django application and Celery services.
- The **Dockerfile** and **docker-compose.yaml** configure the following services:
  - **Django App**: The main web application.
  - **Redis**: A message broker for Celery.
  - **Celery Worker**: Executes background tasks.
  - **Celery Beat**: Manages task scheduling.

> **Note:** The **SQL Server** is not included in the Docker setup and must be installed and configured **locally**.

---

## Setup Instructions

### Prerequisites
- **Docker** and **Docker Compose**.
- **Microsoft SQL Server** installed locally.
- Django configured to connect to the local SQL Server.

---

### Running the Project

#### Step 1: Clone the Repository
```bash
git clone <repo_url>
cd <repo_directory>
```

#### Step 2: Configure SQL Server
- Install **Microsoft SQL Server** locally.
- Update the `DATABASES` setting in `settings.py` to match your local SQL Server configuration.

Example:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sql_server',
        'NAME': '<database_name>',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '1433',
    }
}
```

#### Step 3: Build and Start Docker Services
- Start the Django app, Redis, and Celery services using Docker:
```bash
docker-compose up --build
```

#### Step 4: Run Database Migrations
- Apply migrations to the SQL Server:
```bash
docker exec -it <container_name> python manage.py migrate
```

#### Step 5: Access the Application
- The Django app will be available at `http://localhost:8000`.

---


---

## Technologies Used
- **Django**: Web application framework.
- **Python 3.9**: Programming language.
- **Microsoft SQL Server**: Local database backend.
- **JWT**: Authentication and authorization.
- **Celery**: Asynchronous task processing.
- **Redis**: Message broker for Celery.
- **Celery Beat**: Scheduled task management.
- **Docker**: Application containerization.

---

## Key Notes
- SQL Server is configured **locally** and is not included as part of the Docker containers.
- Celery and Celery Beat are automatically started within the Docker containers.
- Scheduled tasks run periodically without any additional manual configuration.
- Test the APIs using tools like **Postman** for validation.
```