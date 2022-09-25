from fastapi import FastAPI
from middlewares import process_time
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file
app = FastAPI()

# Adding middleware to the app
app.include_router(process_time.router)
