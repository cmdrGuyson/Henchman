import os
import certifi
from datetime import datetime
from typing import List, Optional, Any
from bunnet import Document, Link, PydanticObjectId, init_bunnet
from pymongo import MongoClient
from pydantic import BaseModel


ca = certifi.where()


MONGO_URL = os.environ.get("MONGO_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")


# Base models
class CurrencyRate(BaseModel):
    code: str
    label: str
    od_buy_rate: float
    tt_buy_rate: float
    tt_sell_rate: float
    updated_at: datetime


# Document models
class CurrencyRateSnapshot(Document):
    rates: List[CurrencyRate]
    origin: str
    created_at: datetime

    class Settings:
        name = "currencyRates"


client = MongoClient(MONGO_URL)
db = client.get_database(name=MONGO_DATABASE_NAME)

init_bunnet(
    database=db,
    document_models=[CurrencyRateSnapshot],
)
