from typing import List
import atexit
from loguru import logger
from fastapi import FastAPI
from pydantic import BaseModel

# Create the FastAPI app
app = FastAPI()

# Define a data model for input if needed (for demonstration purposes)
class InputModel(BaseModel):
    nums: List[int]

@app.get("/")
def hello_world():
    """
    A simple 'Hello, World!' endpoint.
    """
    logger.info("Hello, World! endpoint was called.")
    return {"message": "Hello, World!"}

# Another example endpoint for demonstration
@app.get("/sum")
def sum_numbers(a: int, b: int):
    """
    Sum two numbers provided as query parameters.
    """
    logger.info(f"Summing {a} and {b}")
    return {"sum": a + b}

def main() -> None:
     logger.info("Starting")

     do_something()

     atexit.register(lambda: logger.info("Exiting!"))


def do_something() -> None:
     inputs = [1, 2]
     logger.debug(f"Doing something with {inputs}")
     output = sum_numbers(inputs)
     logger.info(f"Got {output}")


def sum_numbers(nums: List[int]) -> int:
     return sum(nums)

# To run the FastAPI app, use: uvicorn <filename>:app --reload
