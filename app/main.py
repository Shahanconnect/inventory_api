from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import database, models, schemas, crud

models.Base.metadata.create_all = lambda *args, **kwargs: None  # Alembic handles migrations

app = FastAPI(title="Async Inventory Management API")

@app.post("/products/", response_model=schemas.ProductResponse)
async def create_product(product: schemas.ProductCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_product(db, product)

@app.get("/products/", response_model=list[schemas.ProductResponse])
async def list_products(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_products(db, skip, limit)

@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_product(db, product_id)

@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
async def update_product(product_id: int, product: schemas.ProductUpdate, db: AsyncSession = Depends(database.get_db)):
    return await crud.update_product(db, product_id, product)

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.delete_product(db, product_id)

@app.post("/stock/", response_model=schemas.StockTransactionResponse)
async def create_transaction(tx: schemas.StockTransactionCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_stock_transaction(db, tx)

@app.get("/stock/", response_model=list[schemas.StockTransactionResponse])
async def list_transactions(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_all_transactions(db, skip, limit)

@app.get("/stock/product/{product_id}", response_model=list[schemas.StockTransactionResponse])
async def get_transactions(product_id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_transactions_by_product(db, product_id)
