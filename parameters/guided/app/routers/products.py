from fastapi import APIRouter, HTTPException, Query, Path
from app.schemas.product import ProductResponse, Category, SortField
from typing import Optional

router = APIRouter(prefix="/products", tags=["Products"])

# Sample data (in a real app, this comes from a database)
products_db = [
    {"id": 1, "name": "Laptop", "category": "electronics", "price": 999.99, "rating": 4.5},
    {"id": 2, "name": "Python Book", "category": "books", "price": 39.99, "rating": 4.8},
    {"id": 3, "name": "Headphones", "category": "electronics", "price": 79.99, "rating": 4.2},
    {"id": 4, "name": "T-Shirt", "category": "clothing", "price": 24.99, "rating": 3.9},
    {"id": 5, "name": "Coffee Beans", "category": "food", "price": 14.99, "rating": 4.7},
    {"id": 6, "name": "FastAPI Book", "category": "books", "price": 44.99, "rating": 4.9},
]

@router.get("/", response_model=list[ProductResponse])
def list_products(
    category: Optional[Category] = None,
    min_price: float = Query(default=0, ge=0, description="Minimum price filter"),
    max_price: float = Query(default=99999, ge=0, description="Maximum price filter"),
    min_rating: float = Query(default=0, ge=0, le=5, description="Minimum rating (0-5)"),
    sort_by: SortField = SortField.name,
    search: Optional[str] = Query(default=None, min_length=1, max_length=100),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=50),
):
    """List products with filtering, sorting, and pagination."""
    results = products_db.copy()

    # Apply filters
    if category:
        results = [p for p in results if p["category"] == category]
    results = [p for p in results if min_price <= p["price"] <= max_price]
    results = [p for p in results if p["rating"] >= min_rating]
    if search:
        results = [p for p in results if search.lower() in p["name"].lower()]

    # Sort
    results.sort(key=lambda p: p[sort_by.value])

    # Paginate
    total = len(results)
    results = results[skip : skip + limit]

    return results

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int = Path(gt=0, description="The ID of the product")
):
    """Get a specific product by its ID."""
    for product in products_db:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

@router.get("/category/{category}", response_model=list[ProductResponse])
def list_by_category(
    category: Category,
    sort_by: SortField = SortField.name
):
    """Get all products in a specific category."""
    results = [p for p in products_db if p["category"] == category]
    results.sort(key=lambda p: p[sort_by.value])
    return results