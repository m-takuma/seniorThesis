class MetaData:
    class Parameter:
        def __init__(self,
                     date: str,
                     type: str
                    ) -> None:
            self.date = date
            self.type = type
    
    class ResultSet:
        def __init__(self,
                     count: int
                     ) -> None:
            self.count = count
            
    def __init__(self,
                 title: str,
                 parameter: dict,
                 resultset: dict,
                 processDateTime: str,
                 status: str,
                 message: str
                 ) -> None:
        self.title = title
        self.parameter = self.Parameter(**parameter)
        self.resultset = self.ResultSet(**resultset)
        self.processDateTime = processDateTime
        self.status = status
        self.message = message
    
    def is_normal_status(self):
        return self.status == "200"

class Result:
    def __init__(
            self,
            seqNumber,
            docID,
            edinetCode,
            secCode,
            JCN,
            filerName,
            fundCode,
            ordinanceCode,
            formCode,
            docTypeCode,
            periodStart,
            periodEnd,
            submitDateTime,
            docDescription,
            issuerEdinetCode,
            subjectEdinetCode,
            subsidiaryEdinetCode,
            currentReportReason,
            parentDocID,
            opeDateTime,
            withdrawalStatus,
            docInfoEditStatus,
            disclosureStatus,
            xbrlFlag,
            pdfFlag,
            attachDocFlag,
            englishDocFlag,
            csvFlag,
            legalStatus,
            ) -> None:
        self.seqNumber: int = seqNumber
        self.docID: str = docID
        self.edinetCode: str = edinetCode
        self.secCode: str = secCode
        self.JCN: str = JCN
        self.filerName: str = filerName
        self.fundCode: str = fundCode
        self.ordinanceCode: str = ordinanceCode
        self.formCode: str = formCode
        self.docTypeCode: str = docTypeCode
        self.periodStart: str = periodStart
        self.periodEnd: str = periodEnd
        self.submitDateTime: str = submitDateTime
        self.docDescription: str = docDescription
        self.issuerEdinetCode: str = issuerEdinetCode
        self.subjectEdinetCode: str = subjectEdinetCode
        self.subsidiaryEdinetCode: str = subsidiaryEdinetCode
        self.currentReportReason: str = currentReportReason
        self.parentDocID: str = parentDocID
        self.opeDateTime: str = opeDateTime
        self.withdrawalStatus: str = withdrawalStatus
        self.docInfoEditStatus: str = docInfoEditStatus
        self.disclosureStatus: str = disclosureStatus
        self.xbrlFlag: str = xbrlFlag
        self.pdfFlag: str = pdfFlag
        self.attachDocFlag: str = attachDocFlag
        self.englishDocFlag: str = englishDocFlag
        self.csvFlag: str = csvFlag
        self.legalStatus: str = legalStatus