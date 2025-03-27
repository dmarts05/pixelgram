from fastapi import FastAPI

from pixelgram.db import init_db_lifespan

app = FastAPI(lifespan=init_db_lifespan)
