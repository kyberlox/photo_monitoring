from .users import router as users_router
from .locations import router as locations_router
from .images import router as images_router

__all__ = ["users_router", "locations_router", "images_router"]