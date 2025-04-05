from database import core_postgres, core_s3
import asyncio
import sys


async def recreate_tables():
    await core_postgres.drop_tables()
    await core_postgres.create_tables()

if __name__ == "__main__":
    if "--create-tables" in sys.argv:
        asyncio.run(core_postgres.create_tables())

    if "--drop-tables" in sys.argv:
        asyncio.run(core_postgres.drop_tables())

    if "--recreate-tables" in sys.argv:
        asyncio.run(recreate_tables())

    if "--create-bucket" in sys.argv:
        asyncio.run(core_s3.create_bucket())
