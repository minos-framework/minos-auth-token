import logging
from typing import (
    Any,
    Optional,
)
from datetime import (
    datetime,
    timedelta,
)
from uuid import (
    uuid4,
)
import secrets
from aiohttp import (
    ClientConnectorError,
    ClientResponse,
    ClientSession,
    web,
)
from yarl import (
    URL,
)
from sqlalchemy.orm import (
    sessionmaker,
)
from .database.models import (
    Token,
)
from sqlalchemy import (
    exc,
)
from .exceptions import (
    NoTokenException,
)

logger = logging.getLogger(__name__)


async def add_token(request: web.Request) -> web.Response:
    """ Handle Credentials endpoints """

    Session = sessionmaker(bind=request.app["db_engine"])

    s = Session()

    now = datetime.now()
    uuid = uuid4()
    token = secrets.token_hex(20)
    credential = Token(
        uuid=uuid,
        token=token,
        expire=now + timedelta(days=1),
        created_at=now,
        updated_at=now,
    )

    try:
        s.add(credential)
        s.commit()
    except exc.IntegrityError:
        return web.json_response(status=500, text="Error: Token is already taken.")

    s.close()
    return web.json_response({"uuid": str(uuid), "token": token})


async def validate_token(request: web.Request) -> web.Response:
    """ Handle Credentials endpoints """

    try:
        content = await request.json()

        if "token" not in content:
            return web.HTTPBadRequest(text="Wrong data. Provide token.")
    except Exception:
        return web.HTTPBadRequest(text="Wrong data. Provide token.")

    Session = sessionmaker(bind=request.app["db_engine"])

    s = Session()

    r = s.query(Token).filter(Token.token == content["token"]).first()
    s.close()

    if r is not None:
        if r.expire > datetime.now():
            return web.json_response(text="Token valid")
        else:
            return web.json_response(status=400, text="Token expired.")
    else:
        return web.json_response(status=400, text="Token invalid")


async def refresh_token(request: web.Request) -> web.Response:
    try:
        content = await request.json()

        if "token" not in content:
            return web.json_response(status=400, text="Wrong data. Provide token.")
    except Exception:
        return web.json_response(status=400, text="Wrong data. Provide token.")

    Session = sessionmaker(bind=request.app["db_engine"])

    s = Session()

    r = s.query(Token).filter(Token.token == content["token"]).first()


    if r is not None:
        token = secrets.token_hex(20)
        now = datetime.now()

        r.token = token
        r.expire=now + timedelta(days=1)
        r.updated_at = now

        s.commit()
        s.close()

        return web.json_response({"token": token})
    else:
        s.close()
        return web.json_response(status=400, text="Token not found. Provide correct token.")


