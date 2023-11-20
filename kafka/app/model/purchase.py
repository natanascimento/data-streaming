from datetime import datetime
from random import randint
from uuid import uuid4

from pydantic import BaseModel, Field

from app.model import faker


class Purchase(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    username: str = Field(default_factory=faker.user_name)
    currency: str = Field(default_factory=faker.currency_code)
    amount: int = Field(default_factory=lambda: randint(100, 20000))
    created_at: str = Field(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    @staticmethod
    def get():
        return Purchase().model_dump(by_alias=True)