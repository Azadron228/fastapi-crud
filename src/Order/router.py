from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_order(user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()

    return items

@router.post("/")
async def get_all_orders(user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()

    return items

@router.post("/")
async def get_order(user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()

    return items

@router.post("/")
async def update_order(user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()

    return items

@router.post("/")
async def delete_order(user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()

    return items

