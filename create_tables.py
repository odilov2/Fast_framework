from database import ENGINE, Base
from models import Users, Product, Category, Orders

Base.metadata.create_all(ENGINE)
