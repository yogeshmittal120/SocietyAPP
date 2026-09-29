from fastapi import FastAPI

app = FastAPI(
    title="SocietyAPP API",
    version="0.1.0",
    description="Backend API for the SocietyAPP MVP.",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
