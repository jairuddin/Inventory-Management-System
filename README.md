# Inventory Management System API

This API allows for inventory management using Django Rest Framework (DRF), PostgreSQL, and Redis. It supports JWT authentication and CRUD operations on inventory items. Below are the setup instructions, usage, and API details.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Postman Configuration for Automatic JWT Handling](#postman-configuration-for-automatic-jwt-handling)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Redis Caching](#redis-caching)
- [Contributing](#contributing)
- [License](#license)

## Features
- JWT-based authentication and user login/logout.
- CRUD operations for inventory items.
- Redis caching for efficient data retrieval.
- Unit tests for API functionality.

## Requirements
- Python 3.11 or higher
- Django 4.x
- Django Rest Framework
- PostgreSQL
- Redis for caching

## Setup Instructions

Follow these steps to set up and run the project locally:

1. **Clone the repository:**

   git clone <repository-url>
   cd <repository-directory>
Create a virtual environment:


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:



pip install -r requirements.txt
Configure the PostgreSQL database:

Create a database and a user for your app in PostgreSQL.
Update the DATABASES section in settings.py with your database credentials.
Apply database migrations:



python manage.py migrate
Run the development server:


python manage.py runserver

# Usage
User Authentication

# User Registration

Endpoint: POST http://127.0.0.1:8000/api/auth/register/
Method: POST
Request Body:
json

{
  "username": "test",
  "password": "testpassword",
  "email": "test@exa.com"
}

# User Login

Endpoint: POST http://127.0.0.1:8000/api/auth/login/
Method: POST
Request Body:
json

{
  "username": "testuser",
  "password": "testpassword"
}
Response: JWT tokens for authentication.

{
  "access": "your-access-token",
  "refresh": "your-refresh-token"
}


# CRUD Operations for Inventory Items
# Create Item

Endpoint: POST http://127.0.0.1:8000/api/inventron/items/
Method: POST
Request Body:
json

{
  "item_name": "New Item",
  "item_description": "This is a new item.",
  "item_quantity": 5
}

# Get All Items

Endpoint: GET http://127.0.0.1:8000/api/inventron/items/
Method: GET
Get Item by ID

Endpoint: GET http://127.0.0.1:8000/api/inventron/items/{item_id}/
Method: GET
Update Item

Endpoint: PUT http://127.0.0.1:8000/api/inventron/items/{item_id}/
Method: PUT
Request Body:
json

{
  "item_name": "Updated Item",
  "item_description": "This is an updated item.",
  "item_quantity": 15
}
Delete Item

Endpoint: DELETE http://127.0.0.1:8000/api/inventron/items/{item_id}/
Method: DELETE
Response: Success message

Postman Configuration for Automatic JWT Handling
To make it easier to work with JWT tokens in Postman, you can configure Postman to automatically store and use the authentication token from cookies. Here's how to do it:

1. Store JWT Token in Cookies After Login
In the Tests tab of your login request in Postman, add the following script to automatically store the JWT tokens into cookies:

javascript
Copy code
if (pm.response.code === 200) {
    var jsonData = pm.response.json();

    // Set access token in cookies
    pm.cookies.jar().set({
        url: pm.request.url,
        name: 'access_token',
        value: jsonData.access,
        path: '/',
        domain: '127.0.0.1',  // Use your server domain or localhost
        secure: false,  // Set to true in production with HTTPS
        httpOnly: true,
        sameSite: 'Lax'
    });

    // Set refresh token in cookies
    pm.cookies.jar().set({
        url: pm.request.url,
        name: 'refresh_token',
        value: jsonData.refresh,
        path: '/',
        domain: '127.0.0.1',
        secure: false,
        httpOnly: true,
        sameSite: 'Lax'
    });

    // Optionally store the access token in an environment variable
    pm.environment.set('access_token', jsonData.access);
}
2. Automatically Attach JWT Token for Subsequent Requests
For subsequent CRUD requests, add the following script in the Pre-request Script tab of each request to automatically retrieve and attach the token from cookies:

javascript
Copy code
// Retrieve the access token from cookies and set it in the Authorization header
pm.cookies.jar().get({
    url: pm.request.url,
    name: 'access_token'
}, function (error, cookie) {
    if (cookie) {
        pm.request.headers.add({
            key: 'Authorization',
            value: 'Bearer ' + cookie.value
        });
    }
});
Now, after the login request, the access token will be automatically stored in Postman cookies, and the token will be attached to subsequent requests without manual intervention.

3. Refresh Token Logic (Optional)
You can implement token refresh logic in Postman by calling the refresh token endpoint when the access token expires.

javascript
Copy code
pm.cookies.jar().get({
    url: pm.request.url,
    name: 'access_token'
}, function (error, cookie) {
    if (!cookie) {
        // If access token is not found, use the refresh token to get a new access token
        pm.sendRequest({
            url: 'http://127.0.0.1:8000/api/auth/refresh/',
            method: 'POST',
            header: {
                'Content-Type': 'application/json',
            },
            body: {
                mode: 'raw',
                raw: JSON.stringify({
                    "refresh": pm.cookies.jar().get('refresh_token').value
                })
            }
        }, function (err, res) {
            if (res.code === 200) {
                var jsonData = res.json();
                pm.cookies.jar().set({
                    url: pm.request.url,
                    name: 'access_token',
                    value: jsonData.access,
                    path: '/',
                    domain: '127.0.0.1',
                    secure: false,
                    httpOnly: true,
                    sameSite: 'Lax'
                });
            }
        });
    }
});
With this setup, the JWT access token will be automatically refreshed when it expires, and the new token will be attached to your requests.

API Documentation
You can test the API endpoints using Postman or other tools. Use the Authorization header to send the JWT access token:

makefile

Authorization: Bearer <access_token>
Testing
To run unit tests, execute the following command:


python manage.py test
This will run all the tests for CRUD operations, authentication, and caching.

Redis Caching
Redis is used to cache GET requests for inventory items. Ensure Redis is installed and running:


redis-server
Contributing
Contributions are welcome! Please create an issue or submit a pull request for any improvements or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for more information.

vbnet
Copy code

---

### Updates

1. **Correct API Endpoints**: The URLs now reflect the actual project structure (`http://127.0.0.1:8000/api/`).
2. **Postman Configuration**: The steps explain how to use JWT tokens with Postman cookies, allowing them to be automatically attached to subsequent requests.
3. **Refresh Token Logic**: Optional section added to explain how to refresh tokens automatically.

This README should now cover everything related to setting up, using, and testing your project. Let me know if you need any more changes!





