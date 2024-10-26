from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel
from typing import List, Annotated
import src.models as models
from src.database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:4200",
    "http://localhost",
    "http://localhost:8080",
]
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


class BaseProduct(BaseModel):
    name: str
    description: str = None
    stock: int
    price: int
    expiration_date: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/products/", tags=["products"])
async def create_product(product: BaseProduct, db: db_dependency):
    new_product = models.Product(**product.dict())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/products/", tags=["products"])
async def get_products(db: db_dependency, tags=["products"]):
    products = db.query(models.Product).all()
    return products

@app.get("/products/{product_id}", tags=["products"])
async def get_product(product_id: int, db: db_dependency):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", tags=["products"])
async def update_product(product_id: int, product: BaseProduct, db: db_dependency):
    id = int(product_id)
    product_db = db.query(models.Product).filter(models.Product.id == id).first()
    if product_db is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(product_db, key, value)
    db.commit()
    db.refresh(product_db)
    return product_db


@app.delete("/products/{product_id}", tags=["products"])
async def delete_product(product_id: int, db: db_dependency):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return product
