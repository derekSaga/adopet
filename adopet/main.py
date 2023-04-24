from api.v1.api import api_router
from core.config import settings
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title="Adopet")
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
