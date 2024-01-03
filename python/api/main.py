from fastapi import FastAPI
from router import v1

app = FastAPI()
app.include_router(v1)
