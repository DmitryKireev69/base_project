from fastapi import FastAPI
from src.routers.hotels import router as router_hotels


app = FastAPI(
    description='Добро пожаловать в апи!'
)

app.include_router(router_hotels)


# if __name__ == "__main__":
#     uvicorn.run('main:app', host='0.0.0.0', reload=True)
# fastapi dev main.py
# python main.py
# uvicorn main:app --host localhost --port 8000 --reload