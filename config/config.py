""" Configuration file """
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
@dataclass
class Config:
    """ Base configuration class """
    # pylint: disable=invalid-name
    ENVIRONMENT: str
    ACRCLOUD_PERSONAL_ACCESS_TOKEN: str
    ACRCLOUD_ACCESS_KEY: str
    ACRCLOUD_ACCESS_SECRET: str
    ACRCLOUD_HOST: str

    @classmethod
    def get_config(cls):
        """ Factory method for returning the correct config"""
        load_dotenv()
        config = cls(
            ENVIRONMENT=os.getenv('ENVIRONMENT'),
            ACRCLOUD_PERSONAL_ACCESS_TOKEN=os.getenv('ACRCLOUD_PERSONAL_ACCESS_TOKEN'),
            ACRCLOUD_ACCESS_KEY=os.getenv('ACRCLOUD_ACCESS_KEY'),
            ACRCLOUD_ACCESS_SECRET=os.getenv('ACRCLOUD_ACCESS_SECRET'),
            ACRCLOUD_HOST=os.getenv('ACRCLOUD_HOST')
        )
        return config
