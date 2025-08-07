from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from . import models, schemas


# -------------------
# Product CRUD
# -------------------
async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    try:
        await db.commit()
        await db.refresh(new_product)
        return new_product
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Product name already exists. Please use a different name.")


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Product).offset(skip).limit(limit))
    return result.scalars().all()


async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(models.Product).filter(models.Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


async def update_product(db: AsyncSession, product_id: int, update_data: schemas.ProductUpdate):
    product = await get_product(db, product_id)
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    try:
        await db.commit()
        await db.refresh(product)
        return product
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Update failed due to duplicate or invalid data.")


async def delete_product(db: AsyncSession, product_id: int):
    product = await get_product(db, product_id)
    await db.delete(product)
    await db.commit()
    return {"message": "Product deleted successfully"}


# -------------------
# Stock CRUD
# -------------------
async def create_stock_transaction(db: AsyncSession, tx: schemas.StockTransactionCreate):
    product = await get_product(db, tx.product_id)

    if tx.transaction_type == models.TransactionType.OUT and product.available_quantity < tx.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    if tx.transaction_type == models.TransactionType.IN:
        product.available_quantity += tx.quantity
    else:
        product.available_quantity -= tx.quantity

    db_tx = models.StockTransaction(**tx.dict())
    db.add(db_tx)

    try:
        await db.commit()
        await db.refresh(db_tx)
        return db_tx
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Transaction could not be recorded. Please try again.")


async def get_all_transactions(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.StockTransaction).offset(skip).limit(limit))
    return result.scalars().all()


async def get_transactions_by_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(models.StockTransaction).filter(models.StockTransaction.product_id == product_id)
    )
    return result.scalars().all()
