from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    rental_price: Optional[int] = None
    category: str  # 'men' or 'women'
    type: str  # 'daily-wear', 'wedding', 'occasion'
    region: Optional[str] = None  # 'pakistani', 'arab', 'turkish', 'malay'
    is_rental: bool = False
    wore_once: bool = False
    fabric_transparency: Optional[int] = None  # 1-5
    prayer_friendly: bool = False
    wudu_compatible: bool = False
    size: Optional[str] = None
    condition: Optional[str] = None  # 'new', 'like-new', 'good', 'fair'
    image_url: Optional[str] = None
    location: Optional[str] = None
    masjid_pickup: bool = False
    available_dates: Optional[List[str]] = None

class ProductCreate(ProductBase):
    user_id: str

class Product(ProductBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class ProductFilter(BaseModel):
    category: Optional[str] = None
    type: Optional[str] = None
    region: Optional[str] = None
    is_rental: Optional[bool] = None
    wore_once: Optional[bool] = None
    prayer_friendly: Optional[bool] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    location: Optional[str] = None
    masjid_pickup: Optional[bool] = None