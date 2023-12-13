from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class UserToBalance(BaseModel):
    user_id: int
    value: int


class UserToPhoto(BaseModel):
    user_id: int
    photoURL: str


class Lot(BaseModel):
    photos: list
    title: str
    category_id: int
    description: str
    base_price: float
    price_step: int
    buyout_price: float
    lot_state: str
    delivery_type: str
    seller_id: int
    address: str


class Stake(BaseModel):
    user_id: int
    lot_id: int
    amount: float


class Review(BaseModel):
    user_id: int
    rate: int


class Like(BaseModel):
    lot_id: int
    user_id: int
