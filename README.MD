# Vendor Management System (VMS)

## Overview

The Vendor Management System (VMS) is designed to manage vendors and their purchase orders efficiently. It includes functionalities for calculating and monitoring various performance metrics such as on-time delivery rate, quality rating average, average response time, and fulfillment rate.

## Technologies Used

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: Django ORM
- **Web Server**: Uvicorn
- **Data Validation**: Pydantic
- **API Documentation**: Swagger (built-in with FastAPI)

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/shoaibchauhan/Vendor-Management-System-with-Performance-Metrics.git
    cd Vendor-Management-System-with-Performance-Metrics
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure PostgreSQL**:

    Create a PostgreSQL database named `VMS` with user `postgres` and password `hello`.

    ```sh
    psql -U postgres
    CREATE DATABASE VMS;
    CREATE USER postgres WITH PASSWORD 'hello';
    GRANT ALL PRIVILEGES ON DATABASE VMS TO postgres;
    ```

5. **Apply Django Migrations**:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Run the FastAPI server**:
    ```sh
    uvicorn main:app --reload
    ```

7. **Access Swagger Documentation**:

    Once the server is running, you can access the interactive API documentation provided by Swagger at:

    ```
    http://127.0.0.1:8000/docs
    ```

### Configuration

Create a `.env` file in the root directory with the following content:

```env
DATABASE_URL=postgresql://postgres:hello@localhost/VMS
