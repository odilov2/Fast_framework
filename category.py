from fastapi import HTTPException, status
from fastapi import APIRouter
from database import session, ENGINE
from models import Category
from fastapi.encoders import jsonable_encoder
from schemas import CategoryModel

session = session(bind=ENGINE)

category_router = APIRouter(prefix="/category")


@category_router.get("/")
async def get_categories(status_code=status.HTTP_200_OK):
    categories = session.query(Category).all()
    data = [
        {
            "id": category.id,
            "name": category.name,
        }
        for category in categories
    ]
    return jsonable_encoder(data)


@category_router.post("/create")
async def create_category(category: CategoryModel):
    check_category = session.query(Category).filter(Category.id == category.id).first()
    if check_category:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Already exists")

    new_category = Category(
        id=category.id,
        name=category.name
    )
    session.add(new_category)
    session.commit()

    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Successfully")


@category_router.get('/{id}')
async def get_category(id: int):
    check_category = session.query(Category).filter(Category.id == id).first()
    if check_category:
        data = {
            "id": check_category.id,
            "name": check_category.name
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


@category_router.put('/{id}')
async def update_category(id: int, category: CategoryModel):
    check_category = session.query(Category).filter(Category.id == id).first()
    if check_category:
        for key, value in category.dict(exclude_unset=True).items():
            setattr(check_category, key, value)
            session.commit()
            return HTTPException(status_code=status.HTTP_200_OK, detail="Successfully")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")


@category_router.delete('/{id}')
async def delete_category(id: int):
    check_category = session.query(Category).filter(Category.id == id).first()
    if check_category:
        session.delete(check_category)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Successfully")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category not found")