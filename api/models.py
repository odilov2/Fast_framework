from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    username = Column(String(50), unique=True)
    email = Column(Text)
    password = Column(Text)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship('Orders', back_populates='users')

    def __repr__(self):
        return self.first_name


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    product = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(Text)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='product')
    orders = relationship('Orders', back_populates='product')


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('Users', back_populates='orders')
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Product', back_populates='orders')

