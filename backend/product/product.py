from fastapi import APIRouter, HTTPException
from typing import List
from product.model.product_model import Product
from product.bll.productBll import create_product, get_products, get_product_by_id, update_product, delete_product

router = APIRouter(tags=["Products"])

@router.get("/products", response_model=List[Product])
async def get_products_endpoint():
    products = get_products()
    return products

@router.post("/products", response_model=Product)
async def add_product_endpoint(product: Product):
    new_product = create_product(product)
    return new_product

@router.put("/products/{id}", response_model=Product)
async def update_product_endpoint(id: int, product: Product):
    updated_rows = update_product(id, product)
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = get_product_by_id(id)
    return updated_product

@router.delete("/products/{id}")
async def delete_product_endpoint(id: int):
    deleted_rows = delete_product(id)
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
