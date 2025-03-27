from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from pixelgram.db import get_session

SessionDependency = Annotated[Session, Depends(get_session)]
"""Dependency to get a SQLModel session."""
