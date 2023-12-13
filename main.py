from fastapi import FastAPI

from schemas import User, Lot, Stake, Review, UserToBalance, UserToPhoto, Like
from services import register, login, new_lot, new_stake, new_review, delete_user, add_balance, update_photo, \
    get_all_lots, get_lot, get_user, like_lot, get_liked_lots, delete_lot

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/register/")
async def register_request(user: User):
    if register(user):
        return {"success": True, "statusCode": 201, "message": "User successfully registered!", "user": user.username}
    else:
        return {"success": False, "statusCode": 400, "message": "Error while register!"}


@app.delete("/delete_user/{user_id}/")
async def delete_user_request(user_id):
    if delete_user(user_id):
        return {"success": True, "statusCode": 201, "message": "User successfully deleted!"}
    else:
        return {"success": False, "statusCode": 400, "message": "Error while register!"}


@app.post("/login/")
async def login_request(user: User):
    login_user = login(user)
    if login_user:
        return {"success": True,
                "statusCode": 200,
                "message": "User logged in successfully",
                "authenticatedUser": login_user
                }
    return {"success": False, "statusCode": 400, "message": "Error while login!"}


@app.post("/new_lot/")
async def new_lot_request(lot: Lot):
    if new_lot(lot=lot):
        return {"success": True,
                "statusCode": 201,
                "message": "Lot has been created!"
                }
    else:
        return {"success": False, "statusCode": 400, "message": "Error creating new lot!"}


@app.post("/{lot_id}/new_stake/")
async def new_stake_request(stake: Stake):
    if new_stake(stake=stake):
        return {"success": True,
                "statusCode": 201,
                "message": "You've placed your bet successfully!",
                }
    else: return {"success": False, "statusCode": 400, "message": "Error while creating new stake!"}


@app.post("/rate/{user_id}")
async def new_review_request(review: Review):
    if new_review(review=review):
        return {"success": True,
                "statusCode": 201,
                "message": "User was rated successfully!",
                }
    else:
        return {"success": False, "statusCode": 400, "message": "Error while creating new review!"}


@app.put("/add_balance/{user_id}")
async def add_balance_request(user: UserToBalance):
    if add_balance(user=user):
        return {"success": True,
                "statusCode": 201,
                "message": "Balance updated",
                }
    else:
        return {"success": False, "statusCode": 400, "message": "Error while updating user balance"}


@app.put("/update_profile/{user_id}")
async def update_profile_request(user: UserToPhoto):
    if update_photo(user=user):
        return {"success": True,
                "statusCode": 201,
                "message": "Profile photo updated!",
                }
    else:
        return {"success": False, "statusCode": 400, "message": "Error while updating user photo"}


@app.get("/get_all_lots")
async def get_all_lots_request():
    all_lots = get_all_lots()
    if all_lots:
        return {"success": True,
                "statusCode": 200,
                "message": "All lots",
                "allLots": all_lots
                }
    return {"success": False, "statusCode": 400, "message": "Error while getting all lots"}


@app.get("/lot/{lot_id}")
async def get_lot_request(lot_id: int):
    lot = get_lot(lot_id)
    if lot:
        return {"success": True,
                "statusCode": 200,
                "message": "Lot searched successfully",
                "lotInfo": lot
                }
    return {"success": False, "statusCode": 400, "message": "Error while getting lot"}


@app.get("/users/{user_id}")
async def get_user_request(user_id: int):
    user = get_user(user_id)
    if user:
        return {"success": True,
                "statusCode": 200,
                "message": "User searched successfully",
                "userInfo": user
                }
    return {"success": False, "statusCode": 400, "message": "Error while getting user"}


@app.post("/like_lot")
async def like_lot_request(like: Like):
    if like_lot(like=like):
        return {"success": True,
                "statusCode": 201,
                "message": "Lot liked",
                }
    else:
        return {"success": False, "statusCode": 400, "message": "Error while lot like"}


@app.get("/get_liked_lots/{user_id}")
async def get_liked_lots_request(user_id: int):
    lots = get_liked_lots(user_id)
    if lots:
        return {"success": True,
                "statusCode": 200,
                "message": "Liked lots searched successfully",
                "likedLots": lots
                }
    return {"success": False, "statusCode": 400, "message": "Error while getting liked lots"}


@app.delete("/delete_lot/{lot_id}/")
async def delete_lot_request(lot_id):
    if delete_lot(lot_id):
        return {"success": True, "statusCode": 201, "message": "Lot successfully deleted!"}
    else:
        return {"success": False, "statusCode": 400, "message": "Error deleting lot"}






