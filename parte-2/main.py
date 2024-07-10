from fastapi import FastAPI
from Controller import router


app = FastAPI()
# Include the routers
app.include_router(router)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8500)

 