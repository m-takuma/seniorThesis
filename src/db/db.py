import sqlite3
from db import const


class db:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(const.DB_NAME, isolation_level="EXCLUSIVE")
        self.conn.row_factory = sqlite3.Row
        self.name = const.DB_NAME
        self.__create_table()
    
    def __del__(self):
        self.conn.close()
    
    def __create_table(self):
        result_sql = ('id INTEGER PRIMARY KEY AUTOINCREMENT,'
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
        meta_data_sql = (
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'date TEXT,'
            'count INTEGER,'
            'UNIQUE(date)'
        )
        try:
            self.conn.execute(F"CREATE TABLE {const.DOCS_RESULT_TABLE_NAME}({result_sql})")
            self.conn.commit()
        except:
            pass
        try:
            self.conn.execute(F"CREATE TABLE {const.DOCS_METADATA_TABLE_NAME}({meta_data_sql})")
            self.conn.commit()
        except:
            pass

    def commit(self):
        self.conn.commit()
    
    def create_doc(self, **kwargs):
        self.create_from_dict(kwargs)
    
    def create_doc_by_dict(self, kwargs: dict):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(f':{key}' for key in kwargs.keys())
        # UNIQUE重複時は追加しない
        query = f'INSERT OR IGNORE INTO {const.DOCS_RESULT_TABLE_NAME} ({columns}) VALUES ({placeholders})'
        self.conn.execute(query, kwargs)
    
    def create_metadata(self, date: str, count: int):
        self.__create_metadata_by_dict(date=date, count=count)
    
    def __create_metadata_by_dict(self, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(f':{key}' for key in kwargs.keys())
        # UNIQUE重複時は追加しない
        query = f'INSERT OR IGNORE INTO {const.DOCS_METADATA_TABLE_NAME} ({columns}) VALUES ({placeholders})'
        self.conn.execute(query, kwargs)
    
    def find(self, table_name: str, kwargs: dict):
        conditions = ' AND '.join(f'{key} = :{key}' for key in kwargs.keys())
        query = f'SELECT * FROM {table_name} WHERE {conditions}'
        cursor = self.conn.cursor()
        cursor.execute(query, kwargs)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute(self, query):
        self.conn.execute(query)
