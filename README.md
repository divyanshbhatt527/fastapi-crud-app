# FastAPI MongoDB CRUD Application

This is a FastAPI application that performs CRUD (Create, Read, Update, Delete) operations for two entities: Items and User Clock-In Records. It uses MongoDB as the database, and the application can be deployed locally.

Deployed on : https://fastapi-crud-assessment.koyeb.app/


# Setup and Running Locally

1. Clone the Repository

    git clone <repository-url>
    cd <repository-directory>


2. Set Up Virtual Environment 

    python -m venv venv
    On Windows: venv\Scripts\activate



3. Install Dependencies

    pip install -r requirements.txt


4. Set Up MongoDB
    You can use a MongoDB Atlas cloud instance or a local MongoDB instance.
    Make sure to configure the connection URL in config.py or through environment variables.

5. Run the FastAPI Application

    rn app.main:app --reload


# The API documentation will be available at: http://127.0.0.1:8000/docs

# API Endpoints

# Items API
1. Create a New Item
    URL: /items/create
    Method: POST
    Request Body:
    
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "item_name": "Apple",
        "quantity": 10,
        "expiry_date": "2024-10-30"
    }

    Response:
    
    {
        "id": "some-item-id",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "item_name": "Apple",
        "quantity": 10,
        "expiry_date": "2024-10-30",
        "insert_date": "2024-10-11T15:30:00"
    }

2. Retrieve Item by ID
    URL: /items/{id}
    Method: GET
    Response:

    {
        "id": "some-item-id",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "item_name": "Apple",
        "quantity": 10,
        "expiry_date": "2024-10-30",
        "insert_date": "2024-10-11T15:30:00"
    }

3. Filter Items
    URL: /items/filter
    Method: GET
    Query Parameters:
    email: Filter by email (exact match).
    expiry_date: Filter by items expiring after the provided date.
    insert_date: Filter by items inserted after the provided date.
    quantity: Filter items where quantity is greater than or equal to the provided number.
    Response:
    
    [
        {
            "id": "some-item-id",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "item_name": "Apple",
            "quantity": 10,
            "expiry_date": "2024-10-30",
            "insert_date": "2024-10-11T15:30:00"
        }
    ]

4. Update Item by ID
    URL: /items/{id}
    Method: PUT
    Request Body:
    
    {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "item_name": "Orange",
        "quantity": 15,
        "expiry_date": "2024-11-05"
    }
5. Delete Item by ID
    URL: /items/{id}
    Method: DELETE
    Response:
   
    {
        "message": "Item deleted successfully"
    }


# Clock-In API

1. Create Clock-In Entry
    URL: /clock-in
    Method: POST
    Request Body:
    
    {
        "email": "john.doe@example.com",
        "location": "Office"
    }
    
    Response:
    
    {
        "id": "some-clockin-id",
        "email": "john.doe@example.com",
        "location": "Office",
        "insert_date": "2024-10-11T15:30:00"
    }

2. Retrieve Clock-In Record by ID
    URL: /clock-in/{id}
    Method: GET
    Response:
    
    {
        "id": "some-clockin-id",
        "email": "john.doe@example.com",
        "location": "Office",
        "insert_date": "2024-10-11T15:30:00"
    }
    
3. Filter Clock-In Records
    URL: /clock-in/filter
    Method: GET
    Query Parameters:
    email: Filter by email (exact match).
    location: Filter by location (exact match).
    insert_date: Filter by clock-ins after the provided date.
    Response:
    [
        {
            "id": "some-clockin-id",
            "email": "john.doe@example.com",
            "location": "Office",
            "insert_date": "2024-10-11T15:30:00"
        }
    ]

4. Update Clock-In Record by ID
    URL: /clock-in/{id}
    Method: PUT
    Request Body:
    
    {
        "email": "jane.doe@example.com",
        "location": "Remote"
    }

5. Delete Clock-In Record by ID
    URL: /clock-in/{id}
    Method: DELETE
    Response:
    
    {
        "message": "Clock-in record deleted successfully"
    }


# Error Handling
    400 Bad Request: Invalid input data (e.g., incorrect date format).
    404 Not Found: Item or Clock-In record not found.
    500 Internal Server Error: Database errors or server issues.
