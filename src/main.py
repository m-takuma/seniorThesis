from db.db import db
from edinet_api.response_model import Result
from edinet_api.edinet_api import edinet
def fetch_docs(should_cache = True) -> list[Result]:
    config = edinet.FetchDocsConfiguration()
    docs = edinet.fetch_docs(config=config)
    if should_cache:
        __db = db()
        for result in docs:
            __db.create_from_dict(result.__dict__)
        __db.commit()
        del __db
    return docs

def download_docs(docs: list[Result]):
    edinet.download_files(docs, edinet.FetchDocType.SUBMISSION_DOCUMENTS)

if __name__ == "__main__":
    docs = fetch_docs()
    download_docs(docs)
