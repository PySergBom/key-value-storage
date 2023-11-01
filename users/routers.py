from fastapi import APIRouter, HTTPException, status, Response
from starlette.requests import Request

from api.users.schemas import User
from api.users.users_manager import load_users, pwd_context, save_users

username = ''

router = APIRouter(
    prefix='/auth',
    tags=['Auth & Пользователи'],
)


@router.post("/register/", response_model=User)
def register(user: User):
    users = load_users()
    if user.username in users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким именем уже существует")
    hashed_password = pwd_context.hash(user.password)
    users[user.username] = hashed_password
    save_users(users)
    return {"message": "Вы успешно зарегистрированны"}


@router.post("/login/")
def login(user: User, response: Response):

    users = load_users()
    if user.username not in users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя или пароль")
    stored_password = users[user.username]
    if not pwd_context.verify(user.password, stored_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя или пароль")
    username = user.username
    response.set_cookie(key="user", value=username, httponly=True)
    return {"message": "Вход выполнен успешно"}


@router.get("/me/")
def get_user(request: Request):
    user = request.cookies.get('user')
    return user
