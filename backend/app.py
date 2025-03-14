import random
import logging
import asyncio
import string

from contextlib import asynccontextmanager
from fastapi import FastAPI

print("app.py is imported")
print("app is created")

last_generated_word = None

def generate_random_word(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))

async def generate_word_periodically():
    global last_generated_word
    while True:
        last_generated_word = generate_random_word()
        logging.info(f"Generated new word: {last_generated_word}")
        await asyncio.sleep(10)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        asyncio.create_task(generate_word_periodically())
        logging.info("Periodic word generation started")
        yield
    finally:
        logging.info("Shutting down")
        logging.shutdown()
        
app = FastAPI(lifespan=lifespan)
    
@app.get("/last_word")
async def get_last_generated_word():
    if last_generated_word:
        return {"last_generated_word": last_generated_word}
    else:
        asyncio.create_task(generate_word_periodically())
        return {"message": "No word generated yet"}
    
@app.get("/")
def root():
    return {"message": "Hello World"}

def greet():
    return "Hello"