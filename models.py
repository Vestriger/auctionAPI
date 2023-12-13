import datetime

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, DECIMAL, ARRAY, ForeignKey, \
    CheckConstraint
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy.sql import text


naming_convention = {
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s'
}


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class AbstractUser(Base):
    __abstract__ = True

    username: Mapped[str] = mapped_column(String(63), nullable=False)
    password: Mapped[str] = mapped_column(String(63), nullable=False)
    role: Mapped[str] = mapped_column(String(63), default="user")
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text('TIMEZONE ("utc", now())'), nullable=False)


class User(AbstractUser):
    __tablename__ = 'users'

    photoURL: Mapped[str] = mapped_column(String(255), default="https://api.dicebear.com/7.x/adventurer/svg?seed=Scooter")
    rating: Mapped[Integer] = mapped_column(DECIMAL(2, 1), CheckConstraint('rating >= 0 AND rating <= 5'), default=0)
    balance: Mapped[Integer] = mapped_column(DECIMAL(7, 2), CheckConstraint('balance >= 0'), default=0)
    lots = relationship('Lot', back_populates='seller')
    stakes = relationship('Stake', back_populates='user')


class Review(Base):
    __tablename__ = 'reviews'

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    rate: Mapped[Integer] = mapped_column(DECIMAL(2, 1), CheckConstraint('rate >= 0 AND rate <= 5'))



class Category(Base):
    __tablename__ = 'categories'

    category_name = Column(String(31), nullable=False)


class Lot(Base):
    __tablename__ = 'lots'

    title = Column(String(63), nullable=False)
    description = Column(Text, nullable=False)
    base_price = Column(DECIMAL(7, 2), CheckConstraint('base_price >= 0'), nullable=False)
    price_step = Column(DECIMAL(7, 2), CheckConstraint('price_step >= 0'), default=5)
    buyout_price = Column(DECIMAL(7, 2), CheckConstraint('buyout_price >= 0'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('TIMEZONE ("utc", now())'), nullable=False)
    finish_at = Column(TIMESTAMP)
    photos = Column(ARRAY(String), nullable=False)
    address = Column(String(127), nullable=False)
    seller_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    seller = relationship('User', back_populates='lots')
    category_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"))
    category = relationship('Category')
    lot_state: Mapped[str] = mapped_column(String(63), default="Новое")
    delivery_type = Column(String, nullable=False, default="Почта")
    lot_status: Mapped[str] = mapped_column(String(63), default="active")
    stakes = relationship('Stake', back_populates='lot')


class Stake(Base):
    __tablename__ = 'stakes'

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    user = relationship('User', back_populates='stakes')
    lot_id = Column(Integer, ForeignKey('lots.id', ondelete="CASCADE"))
    lot = relationship('Lot', back_populates='stakes')
    amount = Column(DECIMAL(7, 2), CheckConstraint('amount >= 0'), nullable=False)
    stake_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False)


class Favorites(Base):
    __tablename__ = 'favorites'

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    lot_id = Column(Integer, ForeignKey('lots.id', ondelete="CASCADE"), primary_key=True)