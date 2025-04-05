import asyncio
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator, BinaryIO
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

    async def upload_file(
        self,
        file_key: str,
        file: UploadFile
    ) -> None:
        async with self.get_client() as client:
            try:
                await client.put_object(
                    Bucket=self.__bucket_name,
                    Key=file_key,
                    Body=file.file,
                    ContentType=file.content_type if file.content_type is not None else ""
                )
                _log.info("Файл %s загружен", file.filename)
            except Exception as e:
                _log.error("Ошибка загрузки файла %s: %s", file.filename, e)
                raise

    async def download_file(self, file_key: str) -> bytes:
        async with self.get_client() as client:
            try:
                response = await client.get_object(
                    Bucket=self.__bucket_name,
                    Key=file_key
                )
                async with response["Body"] as stream:
                    content = await stream.read()
                _log.info("Файл успешно получен из хранилища", file_key)
                return content
            except Exception as e:
                _log.error(f"Ошибка получения файла {file_key}: {e}")
                raise

    async def delete_file(self, file_key: str) -> None:
        async with self.get_client() as client:
            try:
                await client.delete_object(
                    Bucket=self.__bucket_name,
                    Key=file_key
                )
                _log.info(f"Файл {file_key} успешно удален")
            except Exception as e:
                _log.error(f"Ошибка удаления файла{file_key}: {e}")
                raise
