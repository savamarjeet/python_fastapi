# python_fastapi
=======
# FastAPI Documentation

This repository contains a FastAPI application with API documentation powered by Swagger UI and ReDoc.

## How to Use

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/savamarjeet/python_fastapi.git
   cd python_fastapi
   ```
2. **Create a virtual environment (using Python 3.11 Version):**
   ```bash
   python3.11 -m virtualenv venv
   source venv/Scripts/activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the FastAPI Application:**
   ```bash
   python main.py
   ```
5. **Access API Documentation:**
    - Swagger UI: http://localhost:8000/api/docs  
    - ReDoc: http://localhost:8000/api/redoc

6. **Access OpenAPI JSON Document:**  
  http://localhost:8000/api/openapi.json

7. **Explore the API:**  
  Open the provided URLs in your web browser to explore and interact with the API documentation.
  First call register api to create new user with email and password  
  login with register email and password to get the jwt access token
  using jwt token we can start calling others APIs.
