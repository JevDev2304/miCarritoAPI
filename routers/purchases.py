from fastapi import APIRouter
purchasesRouter = APIRouter(prefix="/purchases",
    tags=["Purchases"])

@purchasesRouter.get('/hello')
def hello_world():
    return 'Hello world'