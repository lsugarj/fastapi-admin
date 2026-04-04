import uvicorn

if __name__ == "__main__":
    from app.core.config import get_settings
    settings = get_settings()

    uvicorn.run("app.main:app", host=settings.app.host, port=settings.app.port, reload=True)