from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def add_item_to_order(user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()

    return items

@router.get("/")
async def delete_item_from_order(user=Depends(auth_wrapper), db: Session = Depends(get_db)):

    async with db as session:
        result = await session.execute(
            select(Item).where(Item.owner_id == user["user_id"])
        )
        items = result.scalars().all()

    return items