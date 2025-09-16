from fastapi import FastAPI

from src.api.database.schema import UserBase, UserCreate

# from ...src.api.database.schema import UserBase, UserCreate

app = FastAPI()


@app.post("/auth/user/create", response_model=UserBase)
async def create_user(user: UserCreate):
    print("User -> ", user)
    return {"message": "User create api"}


@app.get("/auth/login")
async def login():
    return {"message": "User logged in."}
