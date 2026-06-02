from fastapi import FastAPI
from src.routers.hotels import router as router_hotels
from src.routers.auth import router as router_auth
from src.routers.rooms import router as router_rooms


app = FastAPI(
    description='Добро пожаловать в апи!'
)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)


# if __name__ == "__main__":
#     uvicorn.run('main:app', host='0.0.0.0', reload=True)
# fastapi dev main.py
# python main.py
# uvicorn main:app --host localhost --port 8000 --reload