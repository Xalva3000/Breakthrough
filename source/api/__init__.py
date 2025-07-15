__all__ = ("router",)

from fastapi import APIRouter

from .api_v1 import router as api_v1_router

router = APIRouter(prefix="/api")

# Подключение всех роутеров версии 1
router.include_router(api_v1_router)

