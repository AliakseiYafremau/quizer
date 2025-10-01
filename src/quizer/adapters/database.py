import psycopg
from typing import AsyncGenerator


async def get_async_connection(db_url: str) -> psycopg.AsyncConnection:
    return await psycopg.AsyncConnection.connect(db_url)


async def get_async_session(
    connection: psycopg.AsyncConnection,
) -> psycopg.AsyncCursor:
    return connection.cursor()
