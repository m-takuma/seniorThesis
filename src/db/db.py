import sqlite3
from db import const


class db:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(const.DB_NAME, isolation_level="EXCLUSIVE")
        self.name = const.DB_NAME
        self.__create_table()
    
    def __del__(self):
        self.conn.close()
    
    def __create_table(self):
        s = ('id INTEGER PRIMARY KEY AUTOINCREMENT,'
             'seqNumber INTEGER,'
             'docID TEXT NOT NULL,'
             'edinetCode TEXT,'
             'secCode TEXT,'
             'JCN TEXT,'
             'filerName TEXT,'
             'fundCode TEXT,'
             'ordinanceCode TEXT,'
             'formCode TEXT,'
             'docTypeCode TEXT,'
             'periodStart TEXT,'
             'periodEnd TEXT,'
             'submitDateTime TEXT,'
             'docDescription TEXT,'
             'issuerEdinetCode TEXT,'
             'subjectEdinetCode TEXT,'
             'subsidiaryEdinetCode TEXT,'
             'currentReportReason TEXT,'
             'parentDocID TEXT,'
             'opeDateTime TEXT,'
             'withdrawalStatus TEXT,'
             'docInfoEditStatus TEXT,'
             'disclosureStatus TEXT,'
             'xbrlFlag TEXT,'
             'pdfFlag TEXT,'
             'attachDocFlag TEXT,'
             'englishDocFlag TEXT,'
             'csvFlag TEXT,'
             'legalStatus TEXT,'
             'UNIQUE(docID)')
        cursor = self.conn.cursor()
        cursor.execute(F'SELECT COUNT(*) FROM sqlite_master WHERE TYPE="table" AND NAME="{const.DOCS_RESULT_TABLE_NAME}"')
        if cursor.fetchone() == (0,):
            self.conn.execute(F"CREATE TABLE {const.DOCS_RESULT_TABLE_NAME}({s})")
            self.conn.commit()
        cursor.close()

    def commit(self):
        self.conn.commit()
    
    def create(self, **kwargs):
        self.create_from_dict(kwargs)
    
    def create_from_dict(self, kwargs: dict):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(f':{key}' for key in kwargs.keys())
        # UNIQUE重複時は追加しない
        query = f'INSERT OR IGNORE INTO {const.DOCS_RESULT_TABLE_NAME} ({columns}) VALUES ({placeholders})'
        self.conn.execute(query, kwargs)
