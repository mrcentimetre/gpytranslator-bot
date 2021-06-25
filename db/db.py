from tortoise import Tortoise, fields
from tortoise.models import Model


class users(Model):
    user_id = fields.IntField(pk=True)
    chat_lang = fields.TextField()


async def init_db():
    await Tortoise.init(
        db_url="sqlite://userlanguages.sqlite", modules={"models": [__name__]}
    )
    await Tortoise.generate_schemas()
