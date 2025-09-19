from api.v1.app import app as app_v1
from config import settings
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="cartridges")

app.mount("/v1", app_v1)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "__main__:app",
        host=f"{settings.HOST}",
        port=settings.HTTP_PORT,
        reload=True,
        reload_dirs=["source"],
        log_level="debug",
    )
