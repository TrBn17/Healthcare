from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import httpx
import asyncio

router = APIRouter(prefix="/api/pharmacy", tags=["pharmacy"])

BASE_URL = "https://nhathuoclongchau.com.vn/_next/data/eECsLl5TDa7ftOq1cySZ-"

@router.get("/products")
async def get_products(
    category: str = Query(..., description="Category slug (e.g., thuoc-dieu-tri-ung-thu)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(12, ge=1, le=100, description="Items per page")
):
    """
    Proxy endpoint to fetch pharmacy products from Long Chau
    """
    try:
        # Build the URL
        url = f"{BASE_URL}/thuoc/{category}/{category}.json"
        params = {
            "slug": ["thuoc", category, category]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract products from response
            if "pageProps" in data and "data" in data["pageProps"]:
                page_data = data["pageProps"]["data"]
                products = page_data.get("products", [])
                
                # Pagination
                start_idx = (page - 1) * limit
                end_idx = start_idx + limit
                paginated_products = products[start_idx:end_idx]
                
                return {
                    "success": True,
                    "data": {
                        "products": paginated_products,
                        "total": page_data.get("total", len(products)),
                        "page": page,
                        "limit": limit,
                        "totalPages": (len(products) + limit - 1) // limit,
                        "category": page_data.get("cate", {})
                    }
                }
            else:
                return {
                    "success": False,
                    "message": "Invalid response structure"
                }
                
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/categories")
async def get_categories():
    """
    Get list of available pharmacy categories
    """
    categories = [
        {
            "slug": "thuoc-dieu-tri-ung-thu",
            "name": "Thuốc điều trị ung thư",
            "description": "Các loại thuốc điều trị ung thư"
        },
        {
            "slug": "thuoc-giam-dau-ha-sot",
            "name": "Thuốc giảm đau hạ sốt",
            "description": "Thuốc giảm đau và hạ sốt"
        },
        {
            "slug": "thuoc-ho-long-dom",
            "name": "Thuốc ho long đờm",
            "description": "Thuốc điều trị ho và long đờm"
        },
        {
            "slug": "vitamin-va-khoang-chat",
            "name": "Vitamin và khoáng chất",
            "description": "Bổ sung vitamin và khoáng chất"
        },
        {
            "slug": "thuoc-khang-sinh",
            "name": "Thuốc kháng sinh",
            "description": "Các loại thuốc kháng sinh"
        },
        {
            "slug": "thuoc-da-day",
            "name": "Thuốc dạ dày",
            "description": "Thuốc điều trị bệnh dạ dày"
        }
    ]
    
    return {
        "success": True,
        "data": categories
    }


@router.get("/search")
async def search_products(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
):
    """
    Search products by keyword
    """
    try:
        url = f"https://nhathuoclongchau.com.vn/api/products/search"
        params = {
            "q": q,
            "limit": limit
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
                
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error searching: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
