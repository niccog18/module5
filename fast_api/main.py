from fastapi import FastAPI

app = FastAPI() 

#     Create a main.py file with these endpoints:
# GET / — Returns {"message": "Welcome to my first API"}
@app.get("/")
def read_root():
    return {"message": "Welcome to my first API"}

# GET /about — Returns your name, the current module, and a fun fact about yourself
@app.get("/about")
def about():
    return{
        "name": "Nicco",
        "module": "module 5",
        "fun fact": "I love collecting watches and learning about the different complications they can have."
    }

# GET /greet/{name} — Returns a personalized greeting using the path parameter
@app.get("/greet/{name}")
def greet_user(name:str):
    return{"message": f"Hello, {name}! Welcome to FastAPI."}
        
# POST /echo — Accepts a JSON body with a message field (string) and a shout field (boolean, default False). If shout is True, return the message in UPPERCASE.
from pydantic import BaseModel

class EchoRequest(BaseModel):
    message: str
    shout: bool = False

@app.post("/echo")
def echo_message(data: EchoRequest):
    if data.shout:
        return {"message": data.message.upper()}
    return {"message": data.message}

# Run the server with --reload
    # uvicorn main:app --reload

# Test all four endpoints using the Swagger UI at /docs

# Try sending invalid data to /echo (e.g., shout as a string instead of boolean) and observe the automatic validation error

