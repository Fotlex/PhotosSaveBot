from app.database.models import async_session
from app.database.models import PhotoInfo, User
from sqlalchemy import select, update, delete


async def set_user(tg_id) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_photo(file_id: str, name: str) -> None:
    async with async_session() as session:
        session.add(PhotoInfo(name=name, file_id=file_id))
        await session.commit()


async def get_photo_names():
    async with async_session() as session:
        return await session.scalars(select(PhotoInfo))


async def get_photo_to_id(photo_id: int):
    async with async_session() as session:
        return await session.scalar(select(PhotoInfo.file_id).where(PhotoInfo.id == photo_id))


async def rename_photo(new_name: str, photo_id: int):
    async with async_session() as session:
        await session.execute(update(PhotoInfo).where(PhotoInfo.id == photo_id).values(name=new_name))
        await session.commit()


async def delete_photo(photo_id: int):
    async with async_session() as session:
        await session.execute(delete(PhotoInfo).where(PhotoInfo.id == photo_id))
        await session.commit()
