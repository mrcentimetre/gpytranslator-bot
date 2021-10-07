from tortoise import Tortoise, fields
from tortoise.models import Model
from config import db_url


class users(Model):
    user_id = fields.BigIntField(pk=True)
    chat_lang = fields.TextField()


async def init_db():
    await Tortoise.init(db_url=db_url, modules={"models": [__name__]})
    await Tortoise.generate_schemas()
