from fastapi import FastAPI
#from src.middlewares import process_time
from routes import client
import uvicorn


app = FastAPI()

# Adding middleware to the app
# app.include_router(process_time.router)
app.include_router(client.router, prefix="/mockup", tags=["client"])

if __name__ == "__main__":
    config = uvicorn.Config("server:app", port=3232, log_level="info")
    server = uvicorn.Server(config)
    server.run()
