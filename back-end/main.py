from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from models import ProductCreate, Product, ProductFilter
from database import get_supabase
import uuid

app = FastAPI(title="Muslim Clothing Marketplace API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase = get_supabase()

# ========== HEALTH CHECK ==========
@app.get("/")
def read_root():
    return {"message": "Muslim Clothing Marketplace API", "status": "running"}

# ========== PRODUCTS ENDPOINTS ==========

@app.get("/products", response_model=List[dict])
async def get_products(
    category: Optional[str] = None,
    type: Optional[str] = None,
    region: Optional[str] = None,
    is_rental: Optional[bool] = None,
    wore_once: Optional[bool] = None,
    prayer_friendly: Optional[bool] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    location: Optional[str] = None,
    masjid_pickup: Optional[bool] = None,
):
    """
    Get all products with optional filters
    """
    try:
        query = supabase.table("products").select("*")
        
        # Apply filters
        if category:
            query = query.eq("category", category)
        if type:
            query = query.eq("type", type)
        if region:
            query = query.eq("region", region)
        if is_rental is not None:
            query = query.eq("is_rental", is_rental)
        if wore_once is not None:
            query = query.eq("wore_once", wore_once)
        if prayer_friendly is not None:
            query = query.eq("prayer_friendly", prayer_friendly)
        if masjid_pickup is not None:
            query = query.eq("masjid_pickup", masjid_pickup)
        if location:
            query = query.ilike("location", f"%{location}%")
        if min_price:
            query = query.gte("price", min_price)
        if max_price:
            query = query.lte("price", max_price)
        
        response = query.execute()
        return response.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    """
    Get single product by ID
    """
    try:
        response = supabase.table("products").select("*").eq("id", product_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return response.data[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/products", response_model=dict)
async def create_product(product: ProductCreate):
    """
    Create new product listing
    """
    try:
        product_dict = product.dict()
        
        response = supabase.table("products").insert(product_dict).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create product")
        
        return response.data[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/products/{product_id}")
async def update_product(product_id: str, product: ProductCreate):
    """
    Update existing product
    """
    try:
        product_dict = product.dict()
        
        response = supabase.table("products").update(product_dict).eq("id", product_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return response.data[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/products/{product_id}")
async def delete_product(product_id: str):
    """
    Delete product
    """
    try:
        response = supabase.table("products").delete().eq("id", product_id).execute()
        
        return {"message": "Product deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========== SEARCH ENDPOINT ==========

@app.get("/search")
async def search_products(q: str = Query(..., min_length=1)):
    """
    Search products by name or description
    """
    try:
        response = supabase.table("products").select("*").or_(
            f"name.ilike.%{q}%,description.ilike.%{q}%"
        ).execute()
        
        return response.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========== STATS ENDPOINT (For Dashboard) ==========

@app.get("/stats")
async def get_stats():
    """
    Get marketplace statistics
    """
    try:
        # Total products
        total = supabase.table("products").select("id", count="exact").execute()
        
        # Rental products
        rentals = supabase.table("products").select("id", count="exact").eq("is_rental", True).execute()
        
        # Wore once products
        wore_once = supabase.table("products").select("id", count="exact").eq("wore_once", True).execute()
        
        # Wedding items
        wedding = supabase.table("products").select("id", count="exact").eq("type", "wedding").execute()
        
        return {
            "total_products": total.count,
            "rental_available": rentals.count,
            "wore_once_items": wore_once.count,
            "wedding_items": wedding.count
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========== RUN SERVER ==========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)