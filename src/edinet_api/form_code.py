from enum import Enum

class FormCode(Enum):
    """
    様式コードの一部
    Notes
    -
    布令コードが010の場合の様式コード
    """
    SECURITIES_REPORT = "030000"
    """有価証券報告書"""
    AMENDED_SECURITIES_REPORT = "030001"
    """訂正有価証券報告書"""
    QUARTERLY_REPORT = "043000"
    """四半期報告書"""
    AMENDED_QUARTERLY_REPORT = "043001"
    """訂正四半期報告書"""

    def code(self) -> str:
        """様式コードを返す。valueと同じ値"""
        return self.value
    
    def name(self) -> str:
        """様式番号と様式名を返すの名称を返す"""
        if self == FormCode.SECURITIES_REPORT:
            return "第三号様式	有価証券報告書"
        elif self == FormCode.AMENDED_SECURITIES_REPORT:
            return "第三号様式	訂正有価証券報告書"
        elif self == FormCode.QUARTERLY_REPORT:
            return "第四号の三様式	四半期報告書"
        elif self == FormCode.AMENDED_QUARTERLY_REPORT:
            return "第四号の三様式	訂正四半期報告書"
        else:
            raise SystemError("error")

