import requests
from edinet_api import const
import time
from enum import IntEnum
from dateutil import relativedelta
from datetime import date, datetime
import pandas as pd      
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from edinet_api.ordinance_code import OrdinanceCode
from edinet_api.form_code import FormCode
from edinet_api.response_model import MetaData, Result
import os
from dotenv import load_dotenv
from tqdm import tqdm

class edinet:
    class DocsConfiguration:
        def __init__(
                self,
                corporate_name: str = "",
                start_date: date = datetime.now().date() - relativedelta.relativedelta(months=1),
                end_date: date = datetime.now().date(),
                sec_code: str = "",
                ordinance_code: OrdinanceCode = OrdinanceCode.CORPORATE_AFFAIRS,
                form_code: FormCode = FormCode.SECURITIES_REPORT,

                ) -> None:
            self.corporate_name: str = corporate_name
            self.start_date: date = start_date
            self.end_date: date = end_date
            self.sec_code: str = sec_code
            self.ordinance_code: OrdinanceCode = ordinance_code
            self.form_code: FormCode = form_code
    
    class FetchDocType(IntEnum):
        SUBMISSION_DOCUMENTS = 1
        """提出本文書及び監査報告書"""
        PDF = 2
        """PDF形式"""
        ATTACHED_DOCUMENTS = 3
        """代替書面・添付文書"""
        ENGLISH_DOCUMENTS = 4
        """英文ファイル"""
        @property
        def number(self):
            return self.value

    load_dotenv()
    __xbrl_download_path = os.environ.get("XBRL_DOWNLOAD_PATH")

    def __init__(self, xbrl_download_path: str) -> None:
        self.__xbrl_download_path = xbrl_download_path
    
    @classmethod
    def __should_parse_json(cls, config: DocsConfiguration, result: Result):
        ordinance_code_status = result.ordinanceCode == config.ordinance_code.code()
        form_code_status = result.formCode == config.form_code.code()  # noqa: E501
        corporate_name_status = (config.corporate_name == "" and result.filerName == None) or config.corporate_name in result.filerName
        sec_code_status = (config.sec_code == "" and result.secCode == None) or config.sec_code in result.secCode
        return ordinance_code_status and form_code_status and corporate_name_status and sec_code_status
    
    @classmethod
    def fetch_docs(cls, config = DocsConfiguration()) -> list[Result]:
        docs_list: list[Result] = []
        date_list = list(map(lambda x: x.date(), pd.date_range(start=config.start_date, end=config.end_date, freq="D")))

        for i ,d in enumerate(tqdm(date_list)):
            # アクセス制限回避
            time.sleep(2)
            session = requests.Session()
            retries = Retry(total=2,  # リトライ回数
                            backoff_factor=60,  # sleep時間
                            status_forcelist=[403])
            session.mount("https://", HTTPAdapter(max_retries=retries))
            try:
                params = {
                    "date": F"{d}",
                    "type": "2"
                }
                res = session.get(const.EDINET_API_ENDPOINT_DOCS, params=params, timeout=3.5)
                res.raise_for_status()
                json_data = res.json()
                metadata = MetaData(**json_data["metadata"])
                if not metadata.is_normal_status():
                    print(F"{metadata.status}: {metadata.message}")
                    continue
                for num in range(0, metadata.resultset.count):
                    result = Result(**json_data["results"][num])
                    if cls.__should_parse_json(config, result):
                        docs_list.append(result)
            except Exception as err:
                raise Exception(err)
        return docs_list
    

    @classmethod
    def download_file(self, docID: str, type: FetchDocType):
        url = const.EDINET_API_ENDPOINT_BASE + F"documents/{docID}"
        params = {"type": type.number}
        session = requests.Session()
        retries = Retry(total=2,  # リトライ回数
                        backoff_factor=60,  # sleep時間
                        status_forcelist=[403])
        session.mount("https://", HTTPAdapter(max_retries=retries))
        try:
            res = session.get(url, params=params, timeout=3.5)
            res.raise_for_status()
            filename = self.__xbrl_download_path + docID + ".zip"
            with open(filename, "wb") as file:
                for chunk in res.iter_content(chunk_size=1024):
                    file.write(chunk)
        except Exception as err:
            if res.status_code != 404:
                raise Exception(err)
        return
    

    @classmethod
    def download_files(self, docs_list: list[Result], type: FetchDocType):
        for _, doc in enumerate(tqdm(docs_list)):
            #アクセス制限回避
            time.sleep(1)
            self.download_file(doc.docID, type)