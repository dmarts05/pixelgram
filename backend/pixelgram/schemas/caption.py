from pixelgram.schemas.camel_model import CamelModel


class Caption(CamelModel):
    """Base schema for captions."""

    caption: str
