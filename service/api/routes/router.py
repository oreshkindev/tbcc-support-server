from fastapi import APIRouter

from service.api.routes import ticket, user, report, websocket

router = APIRouter()
router.include_router(ticket.router, tags=["ticket"], prefix="/ticket")
router.include_router(user.router, tags=["user"], prefix="/user")
router.include_router(report.router, tags=["report"], prefix="/report")
router.include_router(websocket.router, tags=["broadcast"], prefix="/websocket")
