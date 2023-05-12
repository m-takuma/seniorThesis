import requests
from dateutil import relativedelta
from datetime import date, datetime, timedelta
        

class FetchEdient:
    class DocsConfiguration:
        def __init__(
                self,
                corporate_name: str = "",
                start_date: date = datetime.now().date() - relativedelta.relativedelta(years=10),
                end_date: date = datetime.now().date(),
                sec_code: str = "",
                form_code: str = ""
                ) -> None:
            pass
            
    def __init__(self) -> None:
        pass

    @classmethod
    def fetch_docs(self, config = DocsConfiguration()) -> None:
        pass
    

    
