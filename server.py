from fastapi import FastAPI
from middlewares import process_time, security
from configurations import *
from routes import client
import uvicorn


app = FastAPI()

# Adding middleware to the app
CORS.setup(app)
process_time.setup(app)
security.setup(app)

# Adding routes to the app
app.include_router(client.router, prefix="/mockup", tags=["client"])

if __name__ == "__main__":
    config = uvicorn.Config("server:app", port=3232, log_level="info")
    server = uvicorn.Server(config)
    server.run()
