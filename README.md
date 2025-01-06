# RESTful Blog API

This project is a RESTful API for a blog application built using Flask, SQLAlchemy, and JWT for authentication.

## Features

- User registration and login with password hashing
- JWT-based authentication
- CRUD operations for blog posts
- Many-to-many relationship between posts and categories
- Pagination for fetching posts

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/endxff/restful-blog-api.git
   cd restful-blog-api
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   ```sh
   export FLASK_APP=app/app.py
   export FLASK_ENV=development
   ```

## Usage

1. Initialize the database:

   ```sh
   flask db init
   flask db migrate
   flask db upgrade
   ```

2. Run the application:
   ```sh
   flask run
   ```

## API Endpoints

### User Endpoints

- **Register a new user**

  ```http
  POST /user/register
  ```

  Request body:

  ```json
  {
  	"name": "string",
  	"username": "string",
  	"password": "string"
  }
  ```

- **Login a user**
  ```http
  POST /user/login
  ```
  Request body:
  ```json
  {
  	"username": "string",
  	"password": "string"
  }
  ```

### Post Endpoints

- **Create a new post**

  ```http
  POST /posts/new
  ```

  Request body:

  ```json
  {
  	"title": "string",
  	"subtitle": "string",
  	"content": "string",
  	"user_id": "integer",
  	"categories": ["string"]
  }
  ```

  Requires JWT token in the `Authorization` header.

- **Get posts**
  ```http
  GET /posts
  ```
  Query parameters:
  - `page`: Page number (default: 1)
  - `per_page`: Number of posts per page (default: 2)
  - `order`: Order of posts (`asc` or `desc`)

## Running Tests

1. Run the tests using pytest:
   ```sh
   pytest
   ```

## Configuration

Configuration settings are stored in `app/config.py`. You can modify the database URI and other settings as needed.

## License

This project is licensed under the MIT License.
