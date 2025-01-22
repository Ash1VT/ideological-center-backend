from base64 import b64encode
from typing import Any

from firebase_admin import storage


def upload_image_to_firebase(folder_path: str, id: int, image_url: str, image_filename: str, image: Any) -> str:
    bucket = storage.bucket()
    uid = b64encode(str(id).encode('ascii'))
    image_ext = image_filename.split('.')[-1]

    if image_url:
        image_url = image_url.split('//')[1]
        blob_image_ext = image_url.split('.')[-1]

        image_url = '/'.join(image_url.split('/')[2:-1])
        image_url = f'{image_url}/{uid}.{blob_image_ext}'
        blob = bucket.blob(image_url)
        blob.delete()

    blob = bucket.blob(f'{folder_path}/{uid}.{image_ext}')
    blob.upload_from_file(image)
    blob.make_public()
    return blob.public_url


def upload_file_to_firebase(folder_path: str, id: int, url: str, filename: str, file: Any) -> str:
    bucket = storage.bucket()
    uid = b64encode(str(id).encode('ascii'))
    file_ext = filename.split('.')[-1]

    if url:
        url = url.split('//')[1]
        blob_file_ext = url.split('.')[-1]

        url = '/'.join(url.split('/')[2:-1])
        url = f'{url}/{uid}.{blob_file_ext}'
        blob = bucket.blob(url)
        blob.delete()

    blob = bucket.blob(f'{folder_path}/{uid}.{file_ext}')
    blob.upload_from_file(file)
    blob.make_public()
    return blob.public_url
