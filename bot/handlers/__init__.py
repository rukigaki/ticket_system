from aiogram import Router

from .handlers import router as handler_router
from .callbacks import router as callback_router

router = Router()
router.include_router(handler_router)
router.include_router(callback_router)
