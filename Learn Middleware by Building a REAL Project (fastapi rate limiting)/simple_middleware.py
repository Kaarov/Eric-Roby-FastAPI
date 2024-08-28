from fastapi import FastAPI, Request
import random
import string

app = FastAPI()


@app.middleware("http")
async def request_id_logging(request: Request, call_next):
    response = await call_next(request)
    random_letters = "".join(random.choice(string.ascii_letters) for _ in range(10))
    print(f"Log {random_letters}")
    response.headers["X-Request-ID"] = random_letters
    return response


@app.get("/")
async def say_hi():
    return "Hello World!"
