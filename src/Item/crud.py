def create_item(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return

def get_all_items(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return

def get_item(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return

def update_item(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return

def delete_item(email):
    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()
    return


