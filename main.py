from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers.products import productsRouter
from routers.purchases import purchasesRouter
from routers.users import usersRouter

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.).
    allow_headers=["*"],  # Permitir todos los headers.
)

app.include_router(purchasesRouter)
app.include_router(productsRouter)
app.include_router(usersRouter)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Cambiado a 0.0.0.0
