from engine.entities.origins.origin_base import OriginBase
import boto3
import chardet
import pandas as pd

class origin_file_aws_s3(OriginBase):
    def __init__(self, origin: dict):
        super().__init__(origin)
        self.loadOriginsData()

    def loadOriginsData(self):
        client = boto3.client(
            's3',
            aws_access_key_id=self.origins['meta']['aws_s3_access_key_id'],
            aws_secret_access_key=self.origins['meta']['aws_s3_secret_access_key'],
            region_name=self.origins['meta']['aws_s3_region']
        )
        bucket_name = self.origins['meta']['aws_s3_bucket']
        object_key = self.origins['meta']['aws_s3_key']
        
        obj = client.get_object(Bucket=bucket_name, Key=object_key)
        body = obj['Body'].read()
        result = chardet.detect(body)
        encoding = result['encoding']
        
        self.data = pd.read_csv(pd.compat.StringIO(body.decode(encoding)), delimiter=';', encoding=encoding)
