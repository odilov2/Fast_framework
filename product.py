from fastapi import HTTPException, status
from fastapi import APIRouter
from database import session, ENGINE
from models import Product
from fastapi.encoders import jsonable_encoder
from schemas import ProductModel

session = session(bind=ENGINE)

product_router = APIRouter(prefix="/products")


@product_router.get("/list")
async def product_data(status_code=status.HTTP_200_OK):
    products = session.query(Product).all()
    data = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category_id": product.category_id,
        }
        for product in products
    ]
    return jsonable_encoder(data)


@product_router.post("/create")
async def create_product(product: ProductModel):
    check_product = session.query(Product).filter(Product.id == product.id).first()
    if check_product:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Already exists")

    new_product = Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id
    )
    session.add(new_product)
    session.commit()

    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Successfully")
