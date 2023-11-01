from fastapi import APIRouter, HTTPException, Response, status
from starlette.requests import Request

from users.schemas import User
from users.users_manager import load_users, pwd_context, save_users

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
)


@router.post("/register/")
def register(user: User):
    users = load_users()
    if user.username in users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this name already exists"
        )
    hashed_password = pwd_context.hash(user.password)
    users[user.username] = hashed_password
    save_users(users)
    return {"message": "You have successfully registered"}


@router.post("/login/")
def login(user: User, response: Response):
    users = load_users()
    if user.username not in users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    stored_password = users[user.username]
    if not pwd_context.verify(user.password, stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    response.set_cookie(key="user", value=user.username, httponly=True)
    return {"message": "Login completed successfully"}


@router.get("/me/")
def get_user(request: Request):
    user = request.cookies.get("user")
    return {"user": f"{user}"} if user else {"message": "The user is not logged in"}


@router.post("/logout/")
def logout(response: Response):
    response.delete_cookie(key="user")
    return {"message": "You are logged out"}
