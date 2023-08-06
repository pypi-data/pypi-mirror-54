import abc 
from daraja_api.conf import AbstractConfig

class AbstractApiClient(abc.ABC):
    def __init__(self, conf:AbstractConfig):
        pass