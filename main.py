from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def root():
    return "Hello"

@app.get("/add")
def add(x: int, y: int) -> int:
    return x + y

@app.get("/welcome/{name}")
def add(name: str) -> str:
    return f"Good luck, {name}!"

@app.get("/phone/{number}")
def phone_number(number):
    return ("phone": number)