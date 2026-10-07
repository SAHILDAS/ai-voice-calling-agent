from fastapi import FastAPI


app = FastAPI(
    title="AI Voice Calling Agent",
    description="Simulated AI voice calling agent for loan customer conversations.",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
