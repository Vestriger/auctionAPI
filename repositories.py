from fastapi import HTTPException
from sqlalchemy import func

from alchemy import session_factory
import models
import schemas


def add_user_to_database(user: schemas.User):
    new_user = models.User(username=user.username, password=user.password)
    with session_factory() as session:
        session.add(new_user)
        session.commit()
    return True


def login_user_from_database(user: schemas.User):
    with session_factory() as session:
        user_from_db = session.query(models.User).filter(models.User.username == user.username,
                                                          models.User.password == user.password).first()
        user_lots_from_db = session.query(models.Lot).filter(models.Lot.seller_id == user_from_db.id).all()
        user_stakes_from_db = session.query(models.Stake).filter(models.Stake.user_id == user_from_db.id).all()
        user_lots = []
        user_stakes = []
        for lot in user_lots_from_db:
            user_lots.append(get_lot_by_id(lot.id))
        for stake in user_stakes_from_db:
            user_stakes.append({
                "stake_on_lot": get_lot_by_id(stake.lot_id),
                "amount": stake.amount,
                "stake_time": stake.stake_time
            })
        user = {
            "id": user_from_db.id,
            "username": user_from_db.username,
            "balance": user_from_db.balance,
            "created_at": user_from_db.created_at,
            "photoURL": user_from_db.photoURL,
            "role": user_from_db.role,
            "lots": user_lots,
            "stakes": user_stakes
        }
        return user


def add_new_lot(lot: schemas.Lot):
    new_lot = models.Lot(
        photos=lot.photos,
        title=lot.title,
        category_id=lot.category_id,
        description=lot.description,
        base_price=lot.base_price,
        price_step=lot.price_step,
        buyout_price=lot.buyout_price,
        lot_state=lot.lot_state,
        delivery_type=lot.delivery_type,
        seller_id=lot.seller_id,
        address=lot.address
    )

    with session_factory() as session:
        session.add(new_lot)
        session.commit()
    return True


def add_new_stake(stake: schemas.Stake):
    new_stake = models.Stake(
        user_id=stake.user_id,
        lot_id=stake.lot_id,
        amount=stake.amount
    )

    with session_factory() as session:
        session.add(new_stake)
        session.commit()
    return True


def add_new_review(review: schemas.Review):
    with session_factory() as session:
        user = session.query(models.User).filter(models.User.id == review.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_review = models.Review(rate=review.rate, user_id=review.user_id)
        session.add(new_review)
        session.commit()

        user.rating = session.query(func.avg(models.Review.rate)).filter(models.Review.user_id == review.user_id).scalar()
        session.commit()
    return True


def delete_user_by_id(user_id):
    with session_factory() as session:
        user = session.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        session.delete(user)
        session.commit()

    return True


def add_balance_to_user(user: schemas.UserToBalance):
    with session_factory() as session:
        user_db = session.query(models.User).filter(models.User.id == user.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_db.balance += user.value
        session.commit()
    return True


def update_user_photo(user: schemas.UserToPhoto):
    with session_factory() as session:
        user_db = session.query(models.User).filter(models.User.id == user.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_db.photoURL = user.photoURL
        session.commit()
    return True


def get_all_lots_from_db():
    all_lots = []

    with session_factory() as session:
        lots_from_db = session.query(models.Lot).all()

    for lot in lots_from_db:
        with session_factory() as session:
            lot_seller = session.query(models.User).filter(models.User.id == lot.seller_id).first()
            if lot_seller:
                lot_seller_dict = {
                                    "username": lot_seller.username,
                                    "photoURL": lot_seller.photoURL,
                                    "rating": lot_seller.rating
                                    }
            else:
                lot_seller_dict = "None"
        all_lots.append({
            "id": lot.id,
            "photos": lot.photos,
            "title": lot.title,
            "base_price": lot.base_price,
            "price_step": lot.price_step,
            "created_at": lot.created_at,
            "finish_at": lot.finish_at,
            "address": lot.address,
            "description": lot.description,
            "lot_state": lot.lot_state,
            "delivery_type": lot.delivery_type,
            "lot_status": lot.lot_status,
            "seller": lot_seller_dict
        })
    return all_lots


def get_lot_by_id(lot_id):
    with session_factory() as session:
        lot_from_db = session.query(models.Lot).filter(models.Lot.id == lot_id).first()
        lot_seller = session.query(models.User).filter(models.User.id == lot_from_db.seller_id).first()
        if lot_seller:
            lot_seller_dict = {
                                "username": lot_seller.username,
                                "photoURL": lot_seller.photoURL,
                                "rating": lot_seller.rating
                                }
        else:
            lot_seller_dict = "None"
        lot = {
            "id": lot_from_db.id,
            "photos": lot_from_db.photos,
            "title": lot_from_db.title,
            "base_price": lot_from_db.base_price,
            "price_step": lot_from_db.price_step,
            "created_at": lot_from_db.created_at,
            "finish_at": lot_from_db.finish_at,
            "address": lot_from_db.address,
            "description": lot_from_db.description,
            "lot_state": lot_from_db.lot_state,
            "delivery_type": lot_from_db.delivery_type,
            "lot_status": lot_from_db.lot_status,
            "seller": lot_seller_dict
        }
    return lot


def get_user_by_id(user_id):
    with session_factory() as session:
        user_from_db = session.query(models.User).filter(models.User.id == user_id).first()
        user_lots_from_db = session.query(models.Lot).filter(models.Lot.seller_id == user_id).all()
        user_stakes_from_db = session.query(models.Stake).filter(models.Stake.user_id == user_id).all()
        user_lots = []
        user_stakes = []
        for lot in user_lots_from_db:
            user_lots.append(get_lot_by_id(lot.id))
        for stake in user_stakes_from_db:
            user_stakes.append({
                "stake_on_lot": get_lot_by_id(stake.lot_id),
                "amount": stake.amount,
                "stake_time": stake.stake_time
            })
        user = {
            "id": user_from_db.id,
            "username": user_from_db.username,
            "balance": user_from_db.balance,
            "created_at": user_from_db.created_at,
            "photoURL": user_from_db.photoURL,
            "role": user_from_db.role,
            "lots": user_lots,
            "stakes": user_stakes
            }

    return user


def like_lot_bd(like: schemas.Like):
    new_like = models.Favorites(user_id=like.user_id, lot_id=like.lot_id)

    with session_factory() as session:
        session.add(new_like)
        session.commit()

    return True


def get_liked_lots_by_id(user_id):
    liked_lots = []
    with session_factory() as session:
        all_liked_lots = session.query(models.Favorites).filter(models.Favorites.user_id == user_id).all()

    for liked_lot in all_liked_lots:
        liked_lots.append(get_lot_by_id(liked_lot.lot_id))

    return liked_lots


def delete_lot_by_id(lot_id):
    with session_factory() as session:
        lot = session.query(models.Lot).filter(models.Lot.id == lot_id).first()
        if not lot:
            raise HTTPException(status_code=404, detail="Lot not found")

        session.delete(lot)
        session.commit()

    return True
