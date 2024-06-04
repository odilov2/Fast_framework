from fastapi import HTTPException, status
from fastapi import APIRouter
from database import session, ENGINE
from models import Product, Category
from fastapi.encoders import jsonable_encoder
from schemas import ProductModel

session = session(bind=ENGINE)

product_router = APIRouter(prefix="/products")


@product_router.get("/")
async def product_data(status_code=status.HTTP_200_OK):
    products = session.query(Product).all()
    data = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": {
                "id": product.category.id,
                "name": product.category.name
            }
        }
        for product in products
    ]
    return jsonable_encoder(data)


@product_router.post("/create")
async def create_product(product: ProductModel):
    check_product_id = session.query(Product).filter(Product.id == product.id).first()
    check_category_id = session.query(Category).filter(Category.id == product.category_id).first()
    if check_product_id:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This product already exists")

    elif check_product_id:
        if check_category_id is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This product already exists or This "
                                                                             "category does not exist")

    elif check_product_id is None:
        if check_category_id:
            new_product = Product(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                category_id=product.category_id
            )
            session.add(new_product)
            session.commit()
            data = [
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "category": {
                        "id": product.category.id,
                        "name": product.category.name
                    }
                }
            ]
            return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="not found")


@product_router.get("/{id}")
async def product_id(id: int):
    check_product = session.query(Product).filter(Product.id == id).first()
    if check_product:
        data = {
            "id": check_product.id,
            "name": check_product.name,
            "description": check_product.description,
            "price": check_product.price,
            "category": {
                "id": check_product.category.id,
                "name": check_product.category.name
            }
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


@product_router.put('/{id}')
async def update_product(id: int, product: ProductModel):
    check_product = session.query(Product).filter(Product.id == id).first()
    check_category_id = session.query(Category).filter(Category.id == product.category_id).first()

    if check_product and check_category_id:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(check_product, key, value)
            session.commit()
            data = {
                "code": 200,
                "message": "Updated product successfully"
            }
            return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product or category not found")


@product_router.delete('/{id}')
async def delete_product(id: int):
    check_product = session.query(Product).filter(Product.id == id).first()
    if check_product:
        session.delete(check_product)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Product deleted successfully")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
