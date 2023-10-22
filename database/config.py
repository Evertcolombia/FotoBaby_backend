#pylint: disable=C0303, E1123, E0401
"""
This module initializes the database connection for the application
It uses Tortoise ORM for database management and FastAPI for API creation.

It defines two functions:
    - init_db        : This function initializes Tortoise ORM by registering it with FastAPI
    - generate_schema: This function generates the database schema using Tortoise ORM
"""

from logging import getLogger

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from core.config import settings

log = getLogger(__name__)

tortoise_config = {
    "connections": {"default": settings.DATABASE_URI},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

def init_db(app: FastAPI) -> None:
    """### Initialize Tortoise ORM for the application.

    Args:
        app (FastAPI): FastAPI application instance
    """

    register_tortoise(
        app,
        config=tortoise_config,
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def generate_schema() -> None:
    """### Generate the database schema using Tortoise ORM.
    """

    log.info("Initializing Tortoise...")
    await Tortoise.init(
        config=tortoise_config
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
