from fastapi import FastAPI
from middlewares import process_time, security
from configurations import *
from routes import client, transactions, darf
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

# Adding middleware to the app
CORS.setup(app)

process_time.setup(app)
security.setup(app)

# Adding routes to the app
app.include_router(client.router, prefix="/mockup", tags=["client"])
app.include_router(transactions.router, tags=["transactions"])
app.include_router(darf.router, tags=["darf"])

if __name__ == "__main__":
    config = uvicorn.Config("server:app", port=3232,
                            log_level="info", host='0.0.0.0')
    server = uvicorn.Server(config)
    server.run()
