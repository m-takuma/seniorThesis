from db.db import db
from edinet_api.fetch_xbrl_file import FetchEdient as edinet
def save_docs_response(should_cache: bool = True):
    config = edinet.DocsConfiguration()
    docs = edinet.fetch_docs(config=config)
    if should_cache:
        __db = db()
        for result in docs:
            print(result.__dict__)
            __db.create_from_dict(result.__dict__)
        __db.commit()
        del __db
    

if __name__ == "__main__":
    save_docs_response()