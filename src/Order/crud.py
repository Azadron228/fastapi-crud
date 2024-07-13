def create_order(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return

def get_all_orders(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return


def get_order(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return


def update_order(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return

def delete_order(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return

