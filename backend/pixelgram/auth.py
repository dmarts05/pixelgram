import uuid
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    InvalidPasswordException,
    UUIDIDMixin,
    exceptions,
    models,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
)
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from httpx_oauth.clients.google import GoogleOAuth2

from pixelgram.db import get_access_token_db, get_user_db
from pixelgram.models.access_token import AccessToken
from pixelgram.models.user import User
from pixelgram.schemas.user import UserCreate
from pixelgram.settings import settings

google_oauth_client = GoogleOAuth2(
    settings.google_auth_client_id,
    settings.google_oauth_client_secret,
)
"""Client for Google OAuth2 authentication."""


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def oauth_callback(
        self,
        oauth_name: str,
        access_token: str,
        account_id: str,
        account_email: str,
        expires_at: Optional[int] = None,
        refresh_token: Optional[str] = None,
        request: Optional[Request] = None,
        *,
        associate_by_email: bool = False,
        is_verified_by_default: bool = False,
    ) -> models.UOAP:  # type: ignore
        oauth_account_dict = {
            "oauth_name": oauth_name,
            "access_token": access_token,
            "account_id": account_id,
            "account_email": account_email,
            "expires_at": expires_at,
            "refresh_token": refresh_token,
        }

        try:
            user = await self.get_by_oauth_account(oauth_name, account_id)
        except exceptions.UserNotExists:
            try:
                # Associate account
                user = await self.get_by_email(account_email)
                if not associate_by_email:
                    raise exceptions.UserAlreadyExists()
                user = await self.user_db.add_oauth_account(user, oauth_account_dict)  # type: ignore
            except exceptions.UserNotExists:
                # Create account
                password = self.password_helper.generate()
                user_dict = {
                    "email": account_email,
                    "username": account_email.split("@")[0],
                    "hashed_password": self.password_helper.hash(password),
                    "is_verified": is_verified_by_default,
                }
                user = await self.user_db.create(user_dict)
                user = await self.user_db.add_oauth_account(user, oauth_account_dict)  # type: ignore
                await self.on_after_register(user, request)
        else:
            # Update oauth
            for existing_oauth_account in user.oauth_accounts:
                if (
                    existing_oauth_account.account_id == account_id
                    and existing_oauth_account.oauth_name == oauth_name
                ):
                    user = await self.user_db.update_oauth_account(  # type: ignore
                        user, existing_oauth_account, oauth_account_dict
                    )

        return user  # type: ignore

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email.split("@")[0] in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")
        if user.username in password:
            raise InvalidPasswordException(
                reason="Password should not contain username"
            )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        pass

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        pass

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        pass


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    """
    Get user manager instance.
    This function is a dependency that can be used in FastAPI routes.
    """
    yield UserManager(user_db)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    """
    Get database strategy for authentication.
    This function is used to create a database strategy for the authentication backend.
    """
    return DatabaseStrategy(
        access_token_db, lifetime_seconds=settings.token_lifetime_minutes * 60
    )


auth_backend = AuthenticationBackend(
    name="cookie",
    transport=CookieTransport(cookie_max_age=settings.token_lifetime_minutes * 60),
    get_strategy=get_database_strategy,
)
"""Authentication backend for cookie-based authentication."""

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
"""FastAPI Users instance for User model."""

current_active_user = fastapi_users.current_user(active=True)
"""Current active user dependency."""
