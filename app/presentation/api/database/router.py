from fastapi import APIRouter

from infrastructure.database.postgres.init import get_db_version


router = APIRouter(
    prefix="/db",
    tags=["DataBase"],
)

@router.get(
    "/version"
)
async def get_database_version() -> str:
    return ""
