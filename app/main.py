from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {
        "Hello": "World",
    }


@app.get("/items/{item_id}")
def read_item(
    item_id: int,
    q: Optional[str] = None,
):
    return {
        "item_id": item_id,
        "q": q,
    }


@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    item: Item,
):
    return {
        "item_name": item.name,
        "item_id": item_id,
    }


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


@app.get("/items/")
async def read_item(
    # 매개변수에 기본값을 부여하면, 자동으로 optional parameter로 간주된다.
    skip: int = 0,
    limit: int = 10,

    # 셋 다 파이썬 관점에서는 유효한 문법이지만, IDE의 타입 추론을 사용하려면 Optional 키워드를 사용하는 것이 권장된다.
    foo = None,
    bar: int = None,
    baz: Optional[int] = None,
):
    return fake_items_db[skip : skip + limit]
