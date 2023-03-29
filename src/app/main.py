# Create a standard FastAPI app

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

# import BackgroundTasks from fastapi

from app.chef_transformer import Chef

app = FastAPI(title="Inspiced", description="Recipe generation API")


import logging

logger = logging.getLogger(__name__)


async def on_startup() -> None:
    logger.info("FastAPI app running...")


app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.add_event_handler("startup", on_startup)


@app.get("/")
def get_root():
    logger.info("FastAPI running in a Docker container")
    return {"message": "FastAPI running in a Docker container"}


@app.post("/generate")
async def generate(items: list[str], background_tasks: BackgroundTasks):
    chef = Chef()

    background_tasks.add_task(chef.generation_function, items)
    return {"message": "Generation in progress.."}
