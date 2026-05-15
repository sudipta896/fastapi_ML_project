from fastapi import APIRouter, FastAPI, HTTPException
from app.cache.redis_cache import get_cached_prediction, set_cached_prediction
from pydantic import BaseModel
from app.core.dependency import get_api_key, get_current_user
from app.servises.model_service import predict_price
from app.core.config import settings

from app.core.exception import register_exception_handlers
from app.middleware.logging_middleware import LoggingMiddleware
from app.api import routs_predict,rout_auth
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(title="Car Price Prediction API")

## Link middleware

app.add_middleware(LoggingMiddleware)

# link endpoints

app.include_router(rout_auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(routs_predict.router, prefix="/api", tags=["Prediction"])


## monitoring using prometheus

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# add exception handlers

register_exception_handlers(app)

