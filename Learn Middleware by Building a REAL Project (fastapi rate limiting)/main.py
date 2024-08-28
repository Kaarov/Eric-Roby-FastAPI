from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict
from typing import Dict

app = FastAPI()


class AdvancedMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rare_limit_records: Dict[str, float] = defaultdict(float)

    async def log_message(self, message: str) -> None:
        print(message)

    async def dispatch(self, request: Request, call_next):
        client_id = request.client.host
        current_time = time.time()
        if current_time - self.rare_limit_records[client_id] < 1:  # 1 request per second limit
            return Response(content="Rate limit exceeded", status_code=429)

        self.rare_limit_records[client_id] = current_time
        path = request.url.path
        await self.log_message(f"Request to {path}")

        # Process the request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Add custom headers without modifying the original headers object
        custom_headers = {"X-Process-Time": str(process_time)}
        for header, value in custom_headers.items():
            response.headers.append(header, value)

        # Asynchronous logging for processing time
        await self.log_message(f"Response fot {path} took {process_time} seconds")

        return response


# Add the advanced middleware to the app
app.add_middleware(AdvancedMiddleware)


@app.get("/")
async def main():
    return {"message": "Hello World!"}
