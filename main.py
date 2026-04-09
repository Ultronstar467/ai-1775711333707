```python
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Modern Calculator App",
    description="A simple FastAPI web app for basic calculations with a modern frontend."
)

# CORS Middleware
# This allows requests from any origin. Essential for local development and sometimes for specific deployment setups.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model for request body validation
class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operator: str

# Define static files directory (for JS and CSS)
# IMPORTANT: For Render, ensure these files are in the root directory alongside main.py
# and index.html, as FileResponse and StaticFiles expect paths relative to the working dir.
# We will explicitly serve index.html with FileResponse and reference style.css/script.js directly
# in index.html without using StaticFiles for simplicity and to avoid path issues on Render
# if 'static' directory isn't managed carefully.
# However, if you have many static assets, StaticFiles is better. For this simple case,
# linking directly in index.html is sufficient and aligns with "simple and beginner-friendly".

# Root endpoint to serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the main HTML page for the calculator."""
    return FileResponse("index.html")

# Endpoint for performing calculations
@app.post("/calculate")
async def calculate(request: CalculationRequest):
    """
    Performs a basic arithmetic calculation based on two numbers and an operator.
    Supports +, -, *, / operators.
    """
    result = None
    error_message = None

    try:
        if request.operator == '+':
            result = request.num1 + request.num2
        elif request.operator == '-':
            result = request.num1 - request.num2
        elif request.operator == '*':
            result = request.num1 * request.num2
        elif request.operator == '/':
            if request.num2 == 0:
                error_message = "Division by zero is not allowed."
            else:
                result = request.num1 / request.num2
        else:
            error_message = f"Invalid operator: {request.operator}. Supported operators are +, -, *, /."

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"

    if error_message:
        return JSONResponse(status_code=400, content={"error": error_message})
    else:
        return {"result": result}

# To run the app locally using an environment variable for port:
# On Linux/macOS: export PORT=8000 && uvicorn main:app --host 0.0.0.0 --port $PORT --reload
# On Windows (cmd): set PORT=8000 && uvicorn main:app --host 0.0.0.0 --port %PORT% --reload
# On Windows (PowerShell): $env:PORT=8000; uvicorn main:app --host 0.0.0.0 --port $env:PORT --reload
# For Render deployment, the start command is already specified in the prompt:
# uvicorn main:app --host 0.0.0.0 --port $PORT
```

---