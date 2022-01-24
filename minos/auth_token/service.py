import logging

from aiohttp import (
    web,
)
from aiomisc.service.aiohttp import (
    AIOHTTPService,
)
from sqlalchemy import (
    create_engine,
)

from .config import (
    TokenConfig,
)
from .database.models import (
    Base,
)
from .handler import (
    add_token,
    refresh_token,
    validate_token,
)

logger = logging.getLogger(__name__)


class TokenRestService(AIOHTTPService):
    def __init__(self, address: str, port: int, config: TokenConfig):
        self.config = config
        self.engine = None
        super().__init__(address, port)

    async def create_application(self) -> web.Application:
        app = web.Application()

        app["config"] = self.config
        self.engine = await self.create_engine()
        await self.create_database()

        app["db_engine"] = self.engine

        app.router.add_route("POST", "/token", add_token)
        app.router.add_route("POST", "/token/validate", validate_token)
        app.router.add_route("POST", "/token/refresh", refresh_token)

        return app

    async def create_engine(self):
        DATABASE_URI = (
            f"postgresql+psycopg2://{self.config.database.user}:{self.config.database.password}@"
            f"{self.config.database.host}:{self.config.database.port}/{self.config.database.dbname}"
        )

        return create_engine(DATABASE_URI)

    async def create_database(self):
        Base.metadata.create_all(self.engine)
