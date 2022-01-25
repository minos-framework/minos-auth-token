import logging
import secrets
from datetime import (
    datetime,
    timedelta,
)
from uuid import (
    uuid4,
)

from aiohttp import (
    web,
)
from sqlalchemy.orm import (
    sessionmaker,
)

from .database.models import (
    Token,
)

logger = logging.getLogger(__name__)


async def add_token(request: web.Request) -> web.Response:
    """ Handle Credentials endpoints """

    Session = sessionmaker(bind=request.app["db_engine"])

    s = Session()

    now = datetime.now()
    uuid = uuid4()
    token = secrets.token_hex(20)
    token_o = Token(uuid=uuid, token=token, expire=now + timedelta(days=1), created_at=now, updated_at=now,)
    s.add(token_o)
    s.commit()
    s.close()
    return web.json_response({"uuid": str(uuid), "token": token})


async def validate_token(request: web.Request) -> web.Response:
    """ Handle Token Validation """

    try:
        token = await _get_authorization_token(request)
    except Exception:
        return web.json_response({"error": "Wrong data. Provide token."}, status=400)

    Session = sessionmaker(bind=request.app["db_engine"])

    s = Session()

    r = s.query(Token).filter(Token.token == token).first()
    s.close()

    if r is not None:
        if r.expire > datetime.now():
            return web.json_response({"message": "Token valid."})

    return web.json_response({"error": "Token invalid."}, status=400,)


async def refresh_token(request: web.Request) -> web.Response:
    """ Refresh Token endpoints """
    try:
        content = await request.json()

        if "token" not in content:
            return web.json_response({"error": "Wrong data. Provide token."}, status=400)
    except Exception:
        return web.json_response({"error": "Wrong data. Provide token."}, status=400)

    Session = sessionmaker(bind=request.app["db_engine"])

    s = Session()

    r = s.query(Token).filter(Token.token == content["token"]).first()

    if r is not None:
        token = secrets.token_hex(20)
        now = datetime.now()

        r.token = token
        r.expire = now + timedelta(days=1)
        r.updated_at = now

        s.commit()
        s.close()

        return web.json_response({"token": token})
    else:
        s.close()
        return web.json_response({"error": "Token not found. Provide correct token."}, status=400)


async def _get_authorization_token(request: web.Request):
    try:
        headers = request.headers
        if "Authorization" in headers and "Bearer" in headers["Authorization"]:
            return headers["Authorization"].split()[1]
        else:
            raise Exception
    except Exception as e:
        raise e
