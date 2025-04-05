import asyncio
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator
from aiobotocore.session import get_session  # type: ignore
from aiobotocore.client import AioBaseClient  # type: ignore
from fastapi import UploadFile
from types_aiobotocore_s3 import S3Client  # Типы для S3
from botocore.config import Config  # type: ignore


_log = logging.getLogger(__name__)


class CoreS3:
    def __init__(
            self,
            user: str,
            password: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.__config = {
            "aws_access_key_id": user,
            "aws_secret_access_key": password,
            "endpoint_url": endpoint_url,
            "config": Config(
                signature_version="s3v4",
                connect_timeout=10,
                retries={"max_attempts": 3},
            ),
            "verify": False,
        }

        self.__bucket_name = bucket_name

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[S3Client]:
        session = get_session()
        async with session.create_client("s3", **self.__config) as client:
            yield client

    async def create_bucket(self) -> None:
        name = self.__bucket_name
        async with self.get_client() as client:
            try:
                # Проверяем существование бакета
                existing_buckets = await client.list_buckets()
                bucket_names = [b["Name"] for b in existing_buckets["Buckets"]]

                if name not in bucket_names:
                    # Создаем бакет
                    await client.create_bucket(Bucket=name)
                    _log.info(f"Бакет {name} создан")
                else:
                    _log.info(f"Бакет {name} уже существует")

            except Exception as e:
                _log.error(f"Ошибка при создании бакета: {e}")
