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
