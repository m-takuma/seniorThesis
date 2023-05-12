from enum import Enum

class OrdinanceCode(Enum):
    """布令コード"""
    CORPORATE_AFFAIRS = "010"
    """企業内容などの開示に関する内閣府令"""
    SYSTEM_ENSURING_APPROPRIATENESS_DOCS = "015"
    """財務計算に関する書類その他の情報の適正性を確保するための体制に関する内閣府令"""
    ISSUERS_OF_FOREIGN_GOVERNMENT_BONDS = "020"
    """外国債等の発行者の開示に関する内閣府令"""
    REGULATED_SECURITIES = "030"
    """特定有価証券の内容等の開示に関する内閣府令"""
    TENDER_OFFER_BY_OTHER_THAN_ISSUER = "040"
    """発行者以外の者による株券等の公開買付けの開示に関する内閣府令"""
    TENDER_OFFER = "050"
    """発行者による上場株券等の公開買付けの開示に関する内閣府令"""
    LARGE_VOLUME_HOLDING_STATUS = "060"
    """株券等の大量保有の状況の開示に関する内閣府令"""

    def code(self) -> str:
        """
        Returns
        -
        布令コードの文字列を返す

        Notes
        -
        valueと同じ値を返す
        """
        return self.value
    
    def name(self) -> str:
        """
        Returns
        -
        布令コードの名称を返す
        """
        if self == OrdinanceCode.CORPORATE_AFFAIRS:
            return "企業内容などの開示に関する内閣府令"
        elif self == OrdinanceCode.SYSTEM_ENSURING_APPROPRIATENESS_DOCS:
            return "財務計算に関する書類その他の情報の適正性を確保するための体制に関する内閣府令"
        elif self == OrdinanceCode.ISSUERS_OF_FOREIGN_GOVERNMENT_BONDS:
            return "外国債等の発行者の開示に関する内閣府令"
        elif self == OrdinanceCode.REGULATED_SECURITIES:
            return "特定有価証券の内容等の開示に関する内閣府令"
        elif self == OrdinanceCode.TENDER_OFFER_BY_OTHER_THAN_ISSUER:
            return "発行者以外の者による株券等の公開買付けの開示に関する内閣府令"
        elif self == OrdinanceCode.TENDER_OFFER:
            return "発行者による上場株券等の公開買付けの開示に関する内閣府令"
        elif self == OrdinanceCode.LARGE_VOLUME_HOLDING_STATUS:
            return "株券等の大量保有の状況の開示に関する内閣府令"
        else:
            raise SystemError("error")
