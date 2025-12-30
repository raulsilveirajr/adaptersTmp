import csv
import os
import time
import chardet
import pandas as pd

from engine.entities.origins.file.local.origin_file_local import OriginFileLocal
from engine.entities.origins.file.ftp.origin_file_ftp import origin_file_ftp
from engine.entities.origins.file.google_cloud.origin_file_google_cloud import origin_file_google_cloud
from engine.entities.origins.file.azure.origin_file_azure import origin_file_azure
from engine.entities.origins.file.aws.origin_file_aws_s3 import origin_file_aws_s3
from engine.tools.logger import log, LogLevel

#TODO: Implementar a lógica de leitura com o DuckDB
class OriginFileLocalCSVByDuckDB(OriginFileLocal):
    def __init__(self, origin: dict):
        super().__init__(origin)
        # self.loadOriginsData()
        self.loadOriginsDataPandas()

    def loadOriginsData(self):
        local_file_path = self.origins["meta"]["meta"]["local_file_path"]
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"File not found: {local_file_path}")
        log(f"Loading data from {local_file_path}")
        with open(
            local_file_path, mode="r", newline="", encoding="iso-8859-1"
        ) as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv, delimiter=";")
            self.data = []
            header = next(leitor_csv)
            for linha in leitor_csv:
                self.data.append(dict(zip(header, linha)))
        log(f"Loaded {len(self.data)} rows (raw) ")

    def loadOriginsDataPandas(self):
        start_time = time.time()
        local_file_path = self.origins["meta"]["meta"]["local_file_path"]
        encoding = "iso-8859-1"
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"File not found: {local_file_path}")

        with open(local_file_path, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']

        try:
            log(f"Loading data from {local_file_path} (pandas)")
            self.data = pd.read_csv(
                local_file_path,
                sep=";",
                encoding=encoding,
                engine="python",
                on_bad_lines="skip",
            )
            log(f"Loaded {len(self.data)} rows (pandas)")
        except Exception as e:
            log(f"Error loading data from {local_file_path}: {e}", LogLevel.ERROR)
        end_time = time.time()
        elapsed_time = end_time - start_time
        # log(self.data, LogLevel.DEBUG)
        log(f"Time taken: {elapsed_time:.2f} seconds (pandas)", LogLevel.DEBUG)
