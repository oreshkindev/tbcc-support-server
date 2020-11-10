from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from service.core.config import PREFIX, DEBUG, PROJECT_NAME, VERSION
from service.core.events import start_handler, stop_handler
from service.api.routes.router import router as api_router


def get_application() -> FastAPI:
    application = FastAPI(
        title=PROJECT_NAME,
        debug=DEBUG,
        version=VERSION,
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/documentation",
        redoc_url=None,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*", "http://localhost:8080/"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler("startup", start_handler(application))
    application.add_event_handler("shutdown", stop_handler(application))

    application.include_router(api_router, prefix=PREFIX)

    return application


app = get_application()