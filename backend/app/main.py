from fastapi import FastAPI

from app.api.routes.customers import router as customers_router
from app.api.routes.loans import router as loans_router


app = FastAPI(
    title="AI Voice Calling Agent",
    description="Simulated AI voice calling agent for loan customer conversations.",
    version="0.1.0",
)


app.include_router(customers_router)
app.include_router(loans_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}