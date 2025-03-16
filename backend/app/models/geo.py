from sqlmodel import SQLModel

class GeoLocation(SQLModel):
    country: str
    state: str | None = None

class GeoLocations(SQLModel):
    data: list[GeoLocation]

# Predefined country and state/province data
COUNTRIES_DATA = {
    "China": ["Beijing", "Shanghai", "Guangdong", "Jiangsu", "Zhejiang", "Sichuan", "Chongqing", "Hubei", "Hunan", "Henan"],
    "United States": ["California", "New York", "Texas", "Florida", "Illinois", "Pennsylvania", "Ohio"],
    "Japan": ["Tokyo", "Osaka", "Aichi", "Kanagawa", "Fukuoka", "Hokkaido", "Kyoto"],
    "United Kingdom": ["England", "Scotland", "Wales", "Northern Ireland"],
    "Canada": ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba"]
}

def get_countries() -> list[str]:
    """Get all countries list"""
    return list(COUNTRIES_DATA.keys())

def get_states(country: str) -> list[str]:
    """Get states/provinces list for a specific country"""
    return COUNTRIES_DATA.get(country, [])