from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()


templates = Jinja2Templates(directory="templates")


users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/", response_class=HTMLResponse)
def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users, "user": None})


@app.get("/user/{user_id}", response_class=HTMLResponse)
def read_user(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user, "users": None})
    raise HTTPException(status_code=404, detail="User was not found")


@app.post("/user/{username}/{age}")
def create_user(username: str, age: int):
    new_id = users[-1].id + 1 if users else 1
    user = User(id=new_id, username=username, age=age)
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail="User was not found")
