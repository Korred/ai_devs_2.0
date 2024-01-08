from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.routes import api_router
from app.core import config

app = FastAPI(
    title="AI Assistant API (AI_DEVS_2.0)",
    version="0.0.1",
    description="-",
    openapi_url="/openapi.json",
    docs_url="/",
)
app.include_router(api_router)

# Sets all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in config.settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Guards against HTTP Host Header attacks
app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.settings.ALLOWED_HOSTS)
