from fastapi import APIRouter
from app.models.geo import GeoLocation, GeoLocations, get_countries, get_states

router = APIRouter()

@router.get("/countries", response_model=list[str])
def list_countries() -> list[str]:
    """获取所有可用的国家列表"""
    return get_countries()

@router.get("/states/{country}", response_model=list[str])
def list_states(country: str) -> list[str]:
    """获取指定国家的州/省列表"""
    return get_states(country)