from google.cloud import storage
import chardet
import pandas as pd
from engine.entities.origins.origin_base import OriginBase
class origin_file_google_cloud(OriginBase):
    def __init__(self, origin: dict):
        super().__init__(origin)
        self.loadOriginsData()

    def loadOriginsData(self):
        client = storage.Client()
        bucket_name = self.origins['meta']['gcs_bucket']
        blob_name = self.origins['meta']['gcs_blob_name']

        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        content = blob.download_as_bytes()
        
        result = chardet.detect(content)
        encoding = result['encoding']
        
        self.data = pd.read_csv(pd.compat.StringIO(content.decode(encoding)), delimiter=';', encoding=encoding)
