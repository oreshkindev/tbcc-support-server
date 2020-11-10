import hashlib
import random
import string
from datetime import datetime, timedelta
from sqlalchemy import and_, desc, func, select

from service.db.database import database
from service.model.user import token_table, user_table
from service.schema import user as user_schema


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user(user_id: int):
    query = user_table.select().where(user_table.c.id == user_id)
    return await database.fetch_one(query)


async def get_user_by_email(email: str):
    query = user_table.select().where(user_table.c.email == email)
    return await database.fetch_one(query)


async def get_users():
    query = (
        select(
            [
                user_table.c.id,
                user_table.c.name,
                user_table.c.lastname,
                user_table.c.tickets_received,
            ]
        )
        .select_from(user_table)
        .order_by(desc(user_table.c.id))
    )
    return await database.fetch_all(query)


async def create_user(user: user_schema.UserCreate):
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = user_table.insert().values(
        email=user.email,
        name=user.name,
        lastname=user.lastname,
        phone=user.phone,
        telegram=user.telegram,
        tickets_received=0,
        hashed_password=f"{salt}${hashed_password}",
    )
    user_id = await database.execute(query)
    token = await create_user_token(user_id)
    token_dict = {"token": token["token"], "expires": token["expires"]}

    return {
        **user.dict(),
        "id": user_id,
        "is_active": True,
        "is_manager": True,
        "tickets_received": 0,
        "token": token_dict,
    }


async def create_user_token(user_id: int):
    query = (
        token_table.insert()
        .values(expires=datetime.now() + timedelta(hours=24), user_id=user_id)
        .returning(token_table.c.token, token_table.c.expires)
    )

    return await database.fetch_one(query)


async def get_user_by_token(token: str):
    query = (
        token_table.join(user_table)
        .select()
        .where(
            and_(token_table.c.token == token, token_table.c.expires > datetime.now())
        )
    )
    return await database.fetch_one(query)


async def update_user_stats(user_id: int):
    query = (
        user_table.update()
        .where(user_table.c.id == user_id)
        .values(tickets_received=user_table.c.tickets_received + int(1))
    )
    return await database.execute(query)