from fastapi import HTTPException, status, Security, Response, APIRouter, Depends
from fastapi import APIRouter
from fastapi_jwt_auth import AuthJWT
from database import session, ENGINE
from models import Users
from schemas import RegisterModel, LoginModel, UsersModel
from werkzeug import security
from fastapi.encoders import jsonable_encoder
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer


access_security = JwtAccessBearer(secret_key="secret_key", auto_error=True)


session = session(bind=ENGINE)

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/")
async def auth(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    users = session.query(Users).all()
    data = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
        }
        for user in users
    ]
    return jsonable_encoder(data)


# @auth_router.get("/")
# async def user_data(status_code=status.HTTP_200_OK):
#     users = session.query(Users).all()
#     data = [
#         {
#             "id": user.id,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "email": user.email,
#             "username": user.username,
#             "is_staff": user.is_staff,
#             "is_active": user.is_active,
#         }
#         for user in users
#     ]
#     return jsonable_encoder(data)


@auth_router.get("/login")
async def login():
    return {"message": "This is login page"}


# @auth_router.post("/login")
# async def login(user: LoginModel):
#     username = session.query(Users).filter(Users.username == user.username).first()
#     if username is None:
#         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     user_check = session.query(Users).filter(Users.username == user.username).first()
#
#     if security.check_password_hash(user_check.password, user.password):
#         return HTTPException(status_code=status.HTTP_200_OK, detail=f"{user.username} logged in")
#
#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username yoki password xato")


@auth_router.post("/login")
async def login(user: LoginModel, Authorize: AuthJWT=Depends()):
    check_user = session.query(Users).filter(Users.username == user.username).first()

    if check_user and security.check_password_hash(check_user.password, user.password):
        access_token = Authorize.create_access_token(subject=check_user.username)
        refresh_token = Authorize.create_refresh_token(subject=check_user.username)
        data = {
            "success": True,
            "code": 200,
            "msg": "Success Login",
            "token": {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }
        return jsonable_encoder(data)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"username yoki password xato")


@auth_router.get("/register")
async def register():
    return {"message": "This is register page"}


@auth_router.post("/register")
async def register(user: RegisterModel):
    username = session.query(Users).filter(Users.username == user.username).first()
    email = session.query(Users).filter(Users.email == user.email).first()

    if email or username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday foydalanuvchi mavjud")

    new_user = Users(
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


@auth_router.get('/{id}')
async def read_user(id: int):
    check_user = session.query(Users).filter(Users.id == id).first()
    if check_user:
        data = {
            "id": check_user.id,
            "first_name": check_user.first_name,
            "last_name": check_user.last_name,
            "username": check_user.username,
            "password": check_user.password,
            "email": check_user.email,
            "is_staff": check_user.is_staff,
            "is_active": check_user.is_active
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@auth_router.put('/{id}')
async def update_user(id: int, user: UsersModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    check_user = session.query(Users).filter(Users.id == id).first()
    if check_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(check_user, key, value)
            session.commit()
            data = {
                "code": 200,
                "message": "Updated user successfully"
            }
            return jsonable_encoder(data)
        # return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password entered")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@auth_router.delete('/{id}')
async def delete_user(id: int):
    check_user = session.query(Users).filter(Users.id == id).first()
    if check_user:
        session.delete(check_user)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="User deleted successfully")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@auth_router.get("/logout")
async def logout():
    return {"message": "This is logout page"}


@auth_router.get("/me")
def read_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    return {"username": credentials["username"], "password": credentials["password"], "role": credentials["role"]}