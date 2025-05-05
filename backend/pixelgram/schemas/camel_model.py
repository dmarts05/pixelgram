from pydantic import BaseModel


def to_camel(string: str) -> str:
    """
    Converts a snake_case string to camelCase.

    Args:
        string: The snake_case string to convert.

    Returns:
        The converted camelCase string.
    """

    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class CamelModel(BaseModel):
    """
    Base model that automatically converts field names to camelCase when dumping to JSON by alias.
    """

    class Config:
        alias_generator = to_camel
        populate_by_name = True
