from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    is_offer: Optional[bool] = None
    foo: str = Field(

        # request body의 파라미터로 취급된다.
        alias="barbaz",

        # 스웨거 문서에서 schema를 보면 나오는 내용.
        title="foo 제목",
        description="foo 설명",
    )


@app.post("/items/")
async def create_item(

    # 매개변수의 타입으로 pydantic model을 지정하면, request body의 타입 구조(?)를 명시할 수 있다.
    item: Item,
):
    item_dict = item.dict()

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({
            "price_with_tax": price_with_tax,
        })

    return item_dict


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

    # 매개변수가 API 경로에도 선언되면, 경로 매개변수로 사용된다.
    item_id: int,

    # 매개변수가 pydantic model 유형으로 선언되면, request body로 사용된다.
    item: Item,

    # 매개변수가 단일 타입으로 선언되면, query parameter로 사용된다.
    q: Optional[str] = None,
):
    result = {
        "item_id": item_id,
        **item.dict(),
    }

    if q:
        result.update({
            "q": q,
        })

    return result


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
