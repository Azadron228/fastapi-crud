import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.router import router


# import asyncio
# import string
# from random import random
# from src.Item.schemas import ItemCreate
# from src.Order.schemas import OrderCreate
# from src.User import crud as user_crud
# from src.Item import crud as item_crud
# from src.Order import crud as order_crud
# from src.User.schemas import UserCreate
# import src.User.model
# import src.Item.model
# from src.database import get_db
#
#
# session = get_db()
#
# async def user():
#     email = "dasd"
#     name = "dawdaf"
#
#     user_create = UserCreate(
#         email=email,
#         password="<PASSWORD>",
#         name=name,
#     )
#     user = await user_crud.create_user(user_create)
#     return user
# async def item(user):
#     item_create = ItemCreate(
#         name = "product v",
#         owner = user,
#         price = 10,
#         description = "product v",
#     )
#
#     item = await item_crud.create_item(item_create)
#     return item
#
# async def order(user):
#     order_create = OrderCreate(
#         user = user
#     )
#     order = order_crud.create_order(order_create)
#     return order
#
#
# async def main():
#     user_instance = await user()
#     # await item(user_instance)
#     # await order(user_instance)
#
# asyncio.run(main())





app = FastAPI(default_response_class=ORJSONResponse)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, )