from fastapi import APIRouter
from connection import  connect_db
productsRouter = APIRouter(prefix="/products",
    tags=["Products"])

@productsRouter.get('/hello')
async def hello_world():
    return await connect_db()