from schemas import User, Lot, Stake, Review
from repositories import add_user_to_database, login_user_from_database, add_new_lot, add_new_stake, add_new_review, \
    delete_user_by_id, add_balance_to_user, update_user_photo, get_all_lots_from_db, get_lot_by_id, get_user_by_id, \
    like_lot_bd, get_liked_lots_by_id, delete_lot_by_id


def register(user: User):
    if add_user_to_database(user=user):
        return True


def login(user: User):
    searched_user = login_user_from_database(user=user)

    if searched_user:
        return searched_user
    else:
        return False


def new_lot(lot: Lot):
    lot = add_new_lot(lot=lot)
    if lot:
        return True
    else:
        return False


def new_stake(stake: Stake):
    stake = add_new_stake(stake=stake)
    if stake:
        return True
    else:
        return False


def new_review(review: Review):
    if add_new_review(review=review):
        return True
    else:
        return False


def delete_user(user_id):
    if delete_user_by_id(user_id):
        return True
    else:
        return False


def add_balance(user):
    if add_balance_to_user(user):
        return True
    else:
        return False


def update_photo(user):
    if update_user_photo(user):
        return True
    else:
        return False


def get_all_lots():
    all_lots = get_all_lots_from_db()

    if all_lots:
        return all_lots
    else:
        return False


def get_lot(lot_id):
    lot = get_lot_by_id(lot_id)

    if lot:
        return lot
    else:
        return False


def get_user(user_id):
    user = get_user_by_id(user_id)

    if user:
        return user
    else:
        return False


def like_lot(like):
    like = like_lot_bd(like)

    if like:
        return True
    else:
        return False


def get_liked_lots(user_id):
    lots = get_liked_lots_by_id(user_id)

    if lots:
        return lots
    else:
        return False


def delete_lot(lot_id):
    if delete_lot_by_id(lot_id):
        return True
    else:
        return False


