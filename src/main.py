from db.db import db
from edinet_api.response_model import Result
from edinet_api.edinet_api import edinet

def fetch_docs(use_chahe = True) -> list[Result]:
    config = edinet.FetchDocsConfiguration()
    docs = edinet.fetch_docs(config=config, use_cache=use_chahe)
    return docs

def download_docs(docs: list[Result]):
    edinet.download_files(docs, edinet.FetchDocType.SUBMISSION_DOCUMENTS)

if __name__ == "__main__":
    docs = fetch_docs()
    download_docs(docs)
