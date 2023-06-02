import os
from dotenv import load_dotenv
load_dotenv()
XBRL_TEMP_PATH = os.environ.get("XBRL_TEMP_PATH")
OUT_PUT_CSV = os.environ.get("OUT_PUT_CSV")