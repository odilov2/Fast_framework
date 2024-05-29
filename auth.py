from fastapi import HTTPException, status
from fastapi import APIRouter
from database import session, ENGINE
from models import User
from schemas import RegisterModel, LoginModel
from werkzeug import security

session = session(bind=ENGINE)

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/")
async def auth():
    return {"message": "This is auth page"}


@auth_router.get("/login")
async def login():
    return {"message": "This is login page"}


@auth_router.post("/login")
async def login(user: LoginModel):
    username = session.query(User).filter(User.username == user.username).first()
    if username is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_check = session.query(User).filter(User.username == user.username).first()

    if security.check_password_hash(user_check.password, user.password):
        return HTTPException(status_code=status.HTTP_200_OK, detail=f"{user.username} logged in")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username yoki password xato")
    # password = session.query(User).filter(User.password == user.password).first()


@auth_router.get("/register")
async def register():
    return {"message": "This is register page"}


@auth_router.post("/register")
async def register(user: RegisterModel):
    username = session.query(User).filter(User.username == user.username).first()
    email = session.query(User).filter(User.email == user.email).first()

    if email or username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday foydalanuvchi mavjud")

    new_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username=user.username,
        password=security.generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )

    session.add(new_user)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="User created successfully")


@auth_router.get("/logout")
async def logout():
    return {"message": "This is logout page"}
