import os
import base64
from fastapi import HTTPException

from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


def _get_client() -> ImageKit:
    priv_key = os.environ.get("IMAGEKIT_PRIVATE_KEY")
    pub_key = os.environ.get("IMAGEKIT_PUBLIC_KEY")
    url_endpoint = os.environ.get("IMAGEKIT_URL_ENDPOINT")

    if not priv_key or not pub_key or not url_endpoint:
        raise HTTPException(
            status_code=500,
            detail="ImageKit environment variables not set"
        )

    return ImageKit(
        private_key=priv_key,
        public_key=pub_key,
        url_endpoint=url_endpoint,
    )


def upload_image(image: bytes, filename: str , folder: str="/products") -> dict:
    client = _get_client()

    encoded = base64.b64encode(image).decode("utf-8")

    options = UploadFileRequestOptions(
        folder=folder,
        is_private=False,
        use_unique_file_name=True,
    )

    response = client.upload(
        file=encoded,
        file_name=filename,
        options=options
    )

    if response.response_metadata.http_status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"ImageKit upload failed: {response.response_metadata}",
        )

    return {
        "name" : response.name,
        "file_id" : response.file_id,
        "url" : response.url,
        "thumbnail_url" : response.thumbnail_url,
    }
    

def upload_images(files: list[tuple[bytes, str]], folder: str = "/products") -> list[str]:
    urls = []
    for file_bytes, filename in files:
        result = upload_image(file_bytes, filename, folder)
        urls.append(result["url"])
    return urls


def delete_image(file_id: str) -> None:
    client = _get_client()

    response = client.delete_file(file_id)

    if response.response_metadata.http_status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"ImageKit delete failed: {response.response_metadata}",
        )