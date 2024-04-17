# University API

This API project provides endpoints for managing student tuition fees and payments in a fictitious university system. It allows students to check their tuition fee status, make payments, and provides administrative functions for managing tuition.

## Features

- User authentication via JWT (JSON Web Tokens).
- Endpoints for querying tuition fee status, paying tuition, and adding tuition for students.
- Separate endpoints for different client applications, such as mobile apps, banking apps, and administrative web interfaces.
- Pagination support for retrieving unpaid tuition status for administrative purposes.
## Data Model (ER diagram)
![SE_4458_ER](https://github.com/OzlemKlc/SE_4458_WEB_API/assets/122043812/30d48a20-00f3-4eed-84c6-952e5db2cf5a)

## Endpoints

### User Authentication

- `POST /v1/login`: Endpoint for authenticating students and generating JWT tokens for authentication.
  - Request Body:
    - `student_no`: Student number (string).

### Student Operations

- `GET /v1/query-tuition`: Endpoint for students to check their tuition fee status.
  - Query Parameters:
    - `student_no`: Student number (string).
- `POST /v1/pay-tuition`: Endpoint for students to pay their tuition fees.
  - Request Body:
    - `student_no`: Student number (string).
    - `term`: Term for which the tuition is being paid (string).

### Administrative Operations

- `POST /v1/add-tuition`: Endpoint for administrators to add tuition fees for students.
  - Request Body:
    - `student_no`: Student number (string).
    - `term`: Term for which the tuition is being added (string).
- `GET /v1/admin/unpaid-tuition-status`: Endpoint for administrators to retrieve a list of students with unpaid tuition fees, supports pagination.
  - Query Parameters:
    - `term`: Term for which the unpaid tuition status is being queried (string).
    - `page`: Page number for pagination (integer, default: 1).
    - `per_page`: Number of items per page (integer, default: 10).

### Banking App Integration

- `GET /v1/banking/query-tuition`: Endpoint for banking apps to query student tuition fee status, requires authentication.
  - Query Parameters:
    - `student_no`: Student number (string).

## Technologies Used

- Flask: Python web framework for building APIs.
- SQLite: Lightweight relational database for storing student and payment data.
- Flask JWT Extended: Flask extension for JSON Web Tokens.
- Flask Swagger UI: Flask extension for adding Swagger UI for API documentation.

## Versioning

This project follows a versioning scheme to ensure backward compatibility and facilitate changes over time. The current version is `v1`. The version is included in the endpoint URLs to allow for future updates without breaking existing client applications.

## Getting Started

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Initialize the SQLite database by running `python app.py`.
4. Start the server using `python app.py`.
5. Access the API endpoints using a client application or tools like cURL or Postman.

# University API

This API project provides endpoints for managing student tuition fees and payments in a fictitious university system. It allows students to check their tuition fee status, make payments, and provides administrative functions for managing tuition.

## Features

- User authentication via JWT (JSON Web Tokens).
- Endpoints for querying tuition fee status, paying tuition, and adding tuition for students.
- Separate endpoints for different client applications, such as mobile apps, banking apps, and administrative web interfaces.
- Pagination support for retrieving unpaid tuition status for administrative purposes.

## Endpoints

### User Authentication

- `POST /v1/login`: Endpoint for authenticating students and generating JWT tokens for authentication.
  - Request Body:
    - `student_no`: Student number (string).

### Student Operations

- `GET /v1/query-tuition`: Endpoint for students to check their tuition fee status.
  - Query Parameters:
    - `student_no`: Student number (string).
- `POST /v1/pay-tuition`: Endpoint for students to pay their tuition fees.
  - Request Body:
    - `student_no`: Student number (string).
    - `term`: Term for which the tuition is being paid (string).

### Administrative Operations

- `POST /v1/add-tuition`: Endpoint for administrators to add tuition fees for students.
  - Request Body:
    - `student_no`: Student number (string).
    - `term`: Term for which the tuition is being added (string).
- `GET /v1/admin/unpaid-tuition-status`: Endpoint for administrators to retrieve a list of students with unpaid tuition fees, supports pagination.
  - Query Parameters:
    - `term`: Term for which the unpaid tuition status is being queried (string).
    - `page`: Page number for pagination (integer, default: 1).
    - `per_page`: Number of items per page (integer, default: 10).

### Banking App Integration

- `GET /v1/banking/query-tuition`: Endpoint for banking apps to query student tuition fee status, requires authentication.
  - Query Parameters:
    - `student_no`: Student number (string).

## Technologies Used

- Flask: Python web framework for building APIs.
- SQLite: Lightweight relational database for storing student and payment data.
- Flask JWT Extended: Flask extension for JSON Web Tokens.
- Flask Swagger UI: Flask extension for adding Swagger UI for API documentation.

## Versioning

This project follows a versioning scheme to ensure backward compatibility and facilitate changes over time. The current version is `v1`. The version is included in the endpoint URLs to allow for future updates without breaking existing client applications.

## Getting Started

1. Clone the repository.
2. Initialize the SQLite database by running `homework_db.db`.
4. Start the server using `python app.py`.
5. Access the API endpoints using a client application or tools like cURL or Postman.

## Video Presentation   
