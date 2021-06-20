from fastapi import APIRouter, Depends
from asyncpg.connection import Connection

from database import _get_connection_from_pool
from model.feature import FeatureCollection
from service.neighborhood_service import NeighborhoodService
from service.apikey_service import APIKeyService

neighborhood_router = APIRouter()

@neighborhood_router.get("/", response_model=FeatureCollection, response_model_exclude_unset=True)
async def neighborhood(
    lat: float, lon: float, apikey: str, conn: Connection = Depends(_get_connection_from_pool)
) -> FeatureCollection:
    exists = await APIKeyService.verify_token(conn, apikey)
    if exists:
        return await NeighborhoodService.get_neighborhood(conn, lat, lon)