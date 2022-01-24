import uuid

from sqlalchemy import (
    TIMESTAMP,
    Column,
    String,
)
from sqlalchemy.dialects.postgresql import (
    UUID,
)
from sqlalchemy.ext.declarative import (
    declarative_base,
)

Base = declarative_base()


class Token(Base):
    __tablename__ = "token"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    token = Column(String, primary_key=True, unique=True)
    expire = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return "Token(uuid='{}', token='{}', expire={}, created_at={}, updated_at={})".format(  # pragma: no cover
            self.uuid, self.token, self.expire, self.created_at, self.updated_at
        )
