from __future__ import annotations

import hashlib
from dataclasses import dataclass

import boto3
from botocore.exceptions import ClientError

from src.adapters.base import BaseAdapter

class S3Error(Exception):
    """Custom exception for S3-related errors."""
    def __init__(self, message: str, original_error: ClientError | None = None):
        super().__init__(message)
        self.original_error = original_error


@dataclass(frozen=True)
class S3UploadResult:
    """Class to represent the result of an S3 upload operation."""
    
    bucket: str
    key: str
    etag: str | None
    content_hash: str

class S3Adapter(BaseAdapter):
    
    def __init__(
        self,
        bucket: str,
        endpoint_url: str | None = None,
        region: str = "us-east-1",
        access_key_id: str | None = None,
        secret_access_key: str | None = None,
    ) -> None:
        
        super().__init__()
        self.bucket = bucket
        self.endpoint_url = endpoint_url
        session = boto3.Session(            
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region,
)
        
        self._client = session.client("s3", endpoint_url=endpoint_url, region_name=region)

    def _content_hash(self, content: bytes) -> str:
        """Return a deterministic SHA-256 hash of the content."""
        return hashlib.sha256(content).hexdigest()
    
    async def upload(
        self,
        key: str,
        content: bytes,
        content_type: str = "text/markdown",
        idempotency_key: str | None = None,
    ) -> S3UploadResult:


        content_hash = self._content_hash(content)
        metadata: dict[str, str] = {
            "content-hash": content_hash,
        }
        if idempotency_key:
            metadata["idempotency-key"] = idempotency_key

        try:
            response = self._client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=content,
                ContentType=content_type,
                Metadata=metadata,)
        
        except ClientError as e:
            msg = f"Failed to upload object {key} to bucket {self._bucket}"
            raise S3Error(msg, e) from e
        
        return S3UploadResult(
            bucket=self._bucket,
            key=key,
            etag=response.get("ETag"),
            content_hash=content_hash,
        )
    
    async def download(self, key: str) -> bytes:

        try:
            response = self._client.get_object(Bucket=self._bucket, Key=key)
        except ClientError as e:
            msg = f"Failed to download object {key} from bucket {self._bucket}"
            raise S3Error(msg, e) from e

        body: bytes = response["Body"].read()
        return body
    
    async def delete(self, key: str) -> None:
        try:
            self._client.delete_object(Bucket=self._bucket, Key=key)
        except ClientError as e:
            msg = f"Failed to delete object {key} from bucket {self._bucket}"
            raise S3Error(msg, e) from e
        
    async def exists(self, key: str) -> bool:
        try:
            self._client.head_object(Bucket=self._bucket, Key=key)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            msg = f"Failed to check existence of object {key} in bucket {self._bucket}"
            raise S3Error(msg, e) from e
        return True