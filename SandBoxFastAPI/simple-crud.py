from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import uvicorn

app = FastAPI()
next_id = 3  # Потому-что уже есть два пользователя


class User(BaseModel):
    name: str
    age: int
    email: EmailStr


class UserPatch(BaseModel):
    name: str | None = None
    age: int | None = None
    email: EmailStr | None = None


users = {
    1: {
        'name': "Valery",
        'age': 26,
        'email': "valery@gmail.com"
    },
    2: {
        'name': "Nastya",
        'age': 23,
        'email': "nastya@gmail.com"
    }
}


@app.get("/users",
         tags=["Пользователи"],
         summary="Получить всех пользователей",
         )
async def get_all_users():
    return users


@app.get("/users/{user_id}",
         tags=["Пользователи"],
         summary="Получить конкретного пользователя",
         )
async def get_user_by_id(user_id: int):
    if user_id in users:
        return users[user_id]
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/users",
          tags=["Пользователи"],
          summary="Добавить нового пользователя",
          )
async def add_user(user: User):
    global next_id

    users[next_id] = {
        'name': user.name,
        'age': user.age,
        'email': str(user.email)  # Приводим к str в явном виде, чтобы PyCharm не ругался на тип EmailStr
    }
    message = f"New user created, id = {next_id}"
    next_id += 1
    return {'success': True, 'message': message}


@app.put("/users/{user_id}",
         tags=["Пользователи"],
         summary="Полностью обновить пользователя",
         )
async def update_user(user_id: int, updated_user: User):
    if user_id in users:
        users[user_id] = {
            'name': updated_user.name,
            'age': updated_user.age,
            'email': str(updated_user.email)  # Приводим к str в явном виде, чтобы PyCharm не ругался на тип EmailStr
        }
        return {'success': True, 'message': f"User (id={user_id}) updated"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.patch("/users/{user_id}",
           tags=["Пользователи"],
           summary="Обновить поля пользователя",
           )
async def patch_user(user_id: int, update: UserPatch):
    update_data = update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    if user_id in users:
        for key, value in update_data.items():
            users[user_id][key] = value
        return {'success': True, "updated_data": users[user_id]}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}",
            tags=["Пользователи"],
            summary="Удалить пользователя",
            )
async def delete_user(user_id: int):
    if user_id in users:
        users.pop(user_id)
        return {'success': True, 'message': f"User (id={user_id}) was deleted"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


if __name__ == '__main__':
    uvicorn.run("simple-crud:app", port=8060, reload=True)
