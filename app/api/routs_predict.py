from fastapi import APIRouter, HTTPException,Depends

from app.cache.redis_cache import get_cached_prediction, set_cached_prediction
from pydantic import BaseModel
from app.core.dependency import get_api_key, get_current_user
from app.servises.model_service import predict_price


router = APIRouter()

class CarFeatures(BaseModel):
    company: str
    year: int
    owner: str
    fuel: str
    seller_type: str
    transmission: str
    km_driven: float
    mileage_mpg: float
    engine_cc: float
    max_power_bhp: float
    torque_nm: float
    seats: float
    
@router.post("/predict") 
def predict(car: CarFeatures, user: str = Depends(get_current_user),  _= Depends(get_api_key)):
    prediction = predict_price(car.model_dump()) 
    return {"predicted_price":  f'{prediction:,.2f}'}
