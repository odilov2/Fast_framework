from fastapi_jwt_auth import AuthJWT

from models import Orders, Users, Product
from schemas import OrderModel, UserOrderModel
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from database import session, ENGINE

session = session(bind=ENGINE)

order_router = APIRouter(prefix="/order")


@order_router.get("/")
async def auth(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    orders = session.query(Orders).all()
    data = [
        {
            "id": order.id,
            "users": {
                "id": order.users.id,
                "first_name": order.users.first_name,
                "last_name": order.users.last_name,
                "username": order.users.username,
                "email": order.users.email,
                "is_staff": order.users.is_staff,
                "is_active": order.users.is_active
            },
            "product_id": {
                "id": order.product.id,
                "name": order.product.name,
                "description": order.product.description,
                "price": order.product.price,
                "category": {
                    "id": order.product.category.id,
                    "name": order.product.category.name
                }
            },
            "count": order.counts
        }
        for order in orders
    ]
    return jsonable_encoder(data)


# @order_router.get("/")
# async def order():
#     orders = session.query(Orders).all()
#     data = [
#         {
#             "id": order.id,
#             "users": {
#                 "id": order.users.id,
#                 "first_name": order.users.first_name,
#                 "last_name": order.users.last_name,
#                 "username": order.users.username,
#                 "email": order.users.email,
#                 "is_staff": order.users.is_staff,
#                 "is_active": order.users.is_active
#             },
#             "product_id": {
#                 "id": order.product.id,
#                 "name": order.product.name,
#                 "description": order.product.description,
#                 "price": order.product.price,
#                 "category": {
#                     "id": order.product.category.id,
#                     "name": order.product.category.name
#                 }
#             },
#             "count": order.counts
#         }
#         for order in orders
#     ]
#     return jsonable_encoder(data)


@order_router.post('/create')
async def order_create(order: OrderModel):
    check_order = session.query(Orders).filter(Orders.id == order.id).first()
    check_user_id = session.query(Users).filter(Users.id == order.users_id).first()
    check_product_id = session.query(Product).filter(Product.id == order.product_id).first()

    if check_order:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already Exists")

    elif check_user_id and check_product_id:
        new_order = Orders(
            id=order.id,
            users_id=order.users_id,
            product_id=order.product_id,
            count=order.count
        )
        session.add(new_order)
        session.commit()

        data = {
            "succes": True,
            "code": 201,
            "message": "Created Order",
            "data": {
                "id": new_order.id,
                "users": {
                    "id": new_order.users.id,
                    "first_name": new_order.users.first_name,
                    "last_name": new_order.users.last_name,
                    "username": new_order.users.username,
                    "email": new_order.users.email,
                    "is_staff": new_order.users.is_staff,
                    "is_active": new_order.users.is_active
                },
                "product_id": {
                    "id": new_order.product.id,
                    "name": new_order.product.name,
                    "description": new_order.product.description,
                    "price": new_order.product.price,
                    "category": {
                        "id": new_order.product.category.id,
                        "name": new_order.product.category.name
                    }
                },
                "count": new_order.counts
            }
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User_id or product_id already exists")


@order_router.get("/{id}")
async def order_get(id: int):
    check_order = session.query(Orders).filter(Orders.id == id).first()
    if check_order:
        data = {
            "succes": True,
            "code": 201,
            "message": "Created Order",
            "data": {
                "id": check_order.id,
                "users": {
                    "id": check_order.users.id,
                    "first_name": check_order.users.first_name,
                    "last_name": check_order.users.last_name,
                    "username": check_order.users.username,
                    "email": check_order.users.email,
                    "is_staff": check_order.users.is_staff,
                    "is_active": check_order.users.is_active
                },
                "product_id": {
                    "id": check_order.product.id,
                    "name": check_order.product.name,
                    "description": check_order.product.description,
                    "price": check_order.product.price,
                    "category": {
                        "id": check_order.product.category.id,
                        "name": check_order.product.category.name
                    }
                },
                "count": check_order.counts,
                "total": check_order.counts * check_order.product.price
            }
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


@order_router.put('/{id}')
async def order_update(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    order = session.query(Orders).filter(Orders.id == id).first()
    check_order = session.query(Orders).filter(Orders.id == order.id).first()
    check_user_id = session.query(Users).filter(Users.id == order.users_id).first()
    check_product_id = session.query(Product).filter(Product.id == order.product_id).first()

    if check_order and check_user_id and check_product_id:
        for key, value in order.dict(exclude_unset=True).items():
            setattr(check_order, key, value)
            session.commit()
            data = {
                "code": 200,
                "message": "Updated order successfully"
            }
            return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


@order_router.delete("/{id}")
async def order_delete(id: int):
    check_order = session.query(Orders).filter(Orders.id == id).first()
    if check_order:
        session.delete(check_order)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Order deleted")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


@order_router.post("/user/order")
async def order_user_get(user_order: UserOrderModel):
    check_user_order = session.query(Users).filter(Users.username == user_order.username).first()
    if check_user_order:
        check_order = session.query(Orders).filter(Orders.users_id == check_user_order.id)
        if check_order:
            data = [
                {
                    "id": order.id,
                    "users": {
                        "id": order.users.id,
                        "first_name": order.users.first_name,
                        "last_name": order.users.last_name,
                        "username": order.users.username,
                        "email": order.users.email,
                        "is_staff": order.users.is_staff,
                        "is_active": order.users.is_active
                    },
                    "product_id": {
                        "id": order.product.id,
                        "name": order.product.name,
                        "description": order.product.description,
                        "price": order.product.price,
                        "category": {
                            "id": order.product.category.id,
                            "name": order.product.category.name
                        }
                    },
                    "count": order.counts
                }
                for order in check_order
            ]
            return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_200_OK, detail="Bu foydalanuvchida buyurtmalar mavjud emas")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday foydalanuvchi mavjud emas")