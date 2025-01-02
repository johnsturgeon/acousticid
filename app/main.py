""" Upload files and fingerprint them, get acousticID and get metadata from musicbrainz """
import json

import aiofiles
import requests

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from acrcloud.recognizer import ACRCloudRecognizer

from config import Config
app = FastAPI()

config = Config.get_config()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication

async def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    """ Check to see if we have an authorized token """
    found_key: str = api_key
    if found_key != 'let-me-in':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


@app.post("/api/get_song_metadata", dependencies=[Depends(api_key_auth)])
async def get_song_metadata(file: UploadFile = File(...)):
    """ API for creating the picks page """
    # await get_acoustic_metadata(file)
    async with aiofiles.open("tmp_file.wav", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    filepath = "tmp_file.wav"
    await acoustid_match(filepath)
    return {"success": "ok"}

async def acoustid_match(filepath):

    acrconfig = {
        'host': config.ACRCLOUD_HOST,
        'access_key': config.ACRCLOUD_ACCESS_KEY,
        'access_secret': config.ACRCLOUD_ACCESS_SECRET,
        'debug': True if config.ENVIRONMENT == 'Development' else False,
        'timeout': 10
    }

    acrcloud: ACRCloudRecognizer = ACRCloudRecognizer(acrconfig)
    results: dict = json.loads(acrcloud.recognize_by_file(filepath, 0))
    if len(results['metadata']['music']):
        acrid: str = results['metadata']['music'][0]['acrid']
        bearer_token: str = config.ACRCLOUD_PERSONAL_ACCESS_TOKEN
        all_metadata = get_acrcloud_metadata(acrid, bearer_token)
        print(all_metadata)
    print(results)


def get_acrcloud_metadata(acrid, bearer_token):
    """
    Fetch metadata for a given ACRID using the ACRCloud Metadata API.

    :param acrid: The ACRID for the resource.
    :param bearer_token: Bearer token for authorization.
    :return: Metadata response from the API.
    """
    url = "https://eu-api-v2.acrcloud.com/api/external-metadata/tracks"
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    params = {"acr_id": acrid}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

