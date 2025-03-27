from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """Base User model that includes fields for email and username."""

    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    """User model that includes fields of the base model and an id and hashed_password field for the database table."""

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str | None = Field(default=None)


class UserPublic(UserBase):
    """Public User model that includes fields of the base model and the id of the user in the database."""

    id: int


class UserCreate(UserBase):
    """User model for creating a new user that includes fields of the base model and a password field."""

    password: str


class UserUpdate(UserBase):
    """
    User model for updating user details.
    Overrides the email and username fields to be optional.
    Includes a password field for updating the user's password.
    """

    email: str | None = None  # type: ignore
    username: str | None = None  # type: ignore
    password: str | None = None
