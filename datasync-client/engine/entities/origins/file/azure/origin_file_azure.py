from engine.entities.origins.origin_base import OriginBase
from azure.storage.blob import BlobServiceClient
import chardet
import pandas as pd

class origin_file_azure(OriginBase):
    def __init__(self, origin: dict):
        super().__init__(origin)
        self.loadOriginsData()

    def loadOriginsData(self):
        connect_str = self.origins['meta']['connection_string']
        container_name = self.origins['meta']['azure_container_name']
        blob_name = self.origins['meta']['azure_blob_name']

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        stream = blob_client.download_blob().readall()
        
        result = chardet.detect(stream)
        encoding = result['encoding']
        
        self.data = pd.read_csv(pd.compat.StringIO(stream.decode(encoding)), delimiter=';', encoding=encoding)
