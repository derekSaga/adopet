import pathlib

import yaml
from api.views.v1.api import api_router
from asgi_correlation_id import CorrelationIdMiddleware
from core.config import settings
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title="Adopet")
app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Request-ID",
)


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    cwd = pathlib.Path(__file__).parent.resolve()
    with open(cwd.parent.joinpath("logging.yaml"), "rt") as file:
        config = yaml.safe_load(file.read())

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        log_level="info",
        reload=True,
        log_config=config,
    )
