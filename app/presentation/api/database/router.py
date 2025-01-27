from fastapi import APIRouter

from infrastructure.database.postgres.init import get_db_version


router = APIRouter(
    prefix="/api",
    tags=["DataBase"],
)
router.add_api_route(path="/db_version", endpoint=get_db_version)
