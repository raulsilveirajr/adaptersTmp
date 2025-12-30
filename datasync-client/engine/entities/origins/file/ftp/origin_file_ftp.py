from ftplib import FTP
from io import BytesIO
import chardet
import pandas as pd
from engine.entities.origins.origin_base import OriginBase

class origin_file_ftp(OriginBase):
    def __init__(self, origin: dict):
        super().__init__(origin)
        self.loadOriginsData()

    def loadOriginsData(self):
        ftp = FTP(self.origins['meta']['ftp_host'])
        ftp.login(user=self.origins['meta']['ftp_user'], passwd=self.origins['meta']['ftp_pass'])
        
        with BytesIO() as f:
            ftp.retrbinary(f'RETR {self.origins["meta"]["ftp_file"]}', f.write)
            f.seek(0)
            content = f.read()
        
        result = chardet.detect(content)
        encoding = result['encoding']
        
        self.data = pd.read_csv(pd.compat.StringIO(content.decode(encoding)), delimiter=';', encoding=encoding)
        ftp.quit()
