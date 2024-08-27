from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller import router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir apenas esta origem
    allow_methods=["GET", "POST"],  # Permitir apenas métodos GET e POST
    allow_headers=[
        "Content-Type",
        "Authorization",
    ],  # Permitir apenas certos cabeçalhos
)
# Include the routers
app.include_router(router)

# teste


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
