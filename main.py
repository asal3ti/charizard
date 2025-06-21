from fastapi import FastAPI
import requests;
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register")
async def register(channel_handle: str):
    print(channel_handle)
    channel = requests.post("", json={"channel_handle": channel_handle})
    return {"message": "User registered"}



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
