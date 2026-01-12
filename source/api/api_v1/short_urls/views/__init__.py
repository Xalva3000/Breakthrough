__all__ = ("router",)


from .views import router
from .details_views import router as detail_router


router.include_router(detail_router)
