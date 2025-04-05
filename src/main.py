import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings

from routers.category import router as r_category
from routers.question import router as r_question
from routers.tag import router as r_tag


_log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _log.info("Start server")
    yield
    _log.info("Stop server")


app = FastAPI(
    lifespan=lifespan,
    root_path="/api"
)

origins = [
    settings.URL_FRONT
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(r_category)
app.include_router(r_question)
app.include_router(r_tag)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
