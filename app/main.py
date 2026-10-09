"""Internal foundation only. No live evidence or commercial endpoints yet."""
import os
from dataclasses import dataclass
from typing import Callable
from fastapi import FastAPI
from fastapi.responses import JSONResponse

@dataclass(frozen=True)
class Settings:
    environment: str = "development"
    database_url: str | None = None

    @classmethod
    def from_environment(cls):
        return cls(os.getenv("FAOS_ENV", "development"), os.getenv("DATABASE_URL"))

    def validate(self):
        if self.environment not in {"development", "test"}:
            raise ValueError("LIVE_OR_UNKNOWN_ENVIRONMENT_NOT_SUPPORTED")
        if self.database_url and not self.database_url.startswith(("postgresql://", "postgresql+psycopg://")):
            raise ValueError("POSTGRESQL_REQUIRED")

def create_app(settings: Settings | None = None, database_probe: Callable[[], bool] | None = None):
    config = settings or Settings.from_environment()
    config.validate()
    app = FastAPI(title="Gavel Foundation", version="0.1.0")
    app.state.settings = config

    @app.get("/health/live")
    def live():
        return {"status": "alive", "version": "0.1.0"}

    @app.get("/health/ready")
    def ready():
        connected = False
        if config.database_url and database_probe is not None:
            try:
                connected = database_probe() is True
            except Exception:
                connected = False
        return JSONResponse(status_code=200 if connected else 503, content={"status": "ready" if connected else "not_ready", "checks": {"database": "passed" if connected else "unverified"}})

    return app

app = create_app()
