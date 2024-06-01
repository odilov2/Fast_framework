from models import Orders, Users, Product
from schemas import OrderModel
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import session, ENGINE

session = session(bind=ENGINE)

order_router = APIRouter(prefix="/order")


@order_router.get("/")
async def order():
    orders = session.query(Orders).all()
    data = [
        {
            "id": order.id,
            "users_id": order.users_id,
            "product_id": order.product_id,
        }
        for order in orders
    ]
    return jsonable_encoder(data)


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
            product_id=order.product_id
        )
        session.add(new_order)
        session.commit()

        return HTTPException(status_code=status.HTTP_201_CREATED, detail="Successfully")
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User_id or product_id already exists")


@order_router.get("/{id}")
async def order_get(id: int):
    check_order = session.query(Orders).filter(Orders.id == id).first()
    if check_order:
        data = {
            "id": check_order.id,
            "users_id": check_order.users_id,
            "product_id": check_order.product_id
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


@order_router.put('/{id}')
async def order_update(id: int, order: OrderModel):
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