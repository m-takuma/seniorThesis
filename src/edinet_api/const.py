import os
from dotenv import load_dotenv
load_dotenv()
EDINET_API_ENDPOINT_BASE = "https://disclosure.edinet-fsa.go.jp/api/v1/"
EDINET_API_ENDPOINT_DOCS = EDINET_API_ENDPOINT_BASE + "documents.json"
XBRL_DOWNLOAD_PATH = os.environ.get("XBRL_DOWNLOAD_PATH")