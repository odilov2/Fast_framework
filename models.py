from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(20), nullable=True)
    username = Column(String(10), unique=True)
    email = Column(Text)
    password = Column(String(15))
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    order = relationship('User', back_populates='user')

    def __repr__(self):
        return self.first_name


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    product = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    description = Column(Text)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='product')
    order = relationship('Order', back_populates='product')


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='order')
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Product', back_populates='order')

