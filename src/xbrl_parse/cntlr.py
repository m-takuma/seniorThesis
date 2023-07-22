from arelle import Cntlr
from arelle.ViewFileDTS import viewDTS
from arelle.ViewFileRelationshipSet import viewRelationshipSet
from arelle.ViewFileRelationshipSet import viewReferences
#from arelle.ViewFileFactList import viewFacts
from arelle.ViewFileFactTable import viewFacts
import const as const
class Cntlr(Cntlr.Cntlr):

    def __init__(self):
        super().__init__()
    
    def run(self, xbrl_file_path: str):
        model_xbrl = self.modelManager.load(xbrl_file_path)
        # viewFacts(model_xbrl, const.OUT_PUT_CSV)
        viewFacts(model_xbrl, const.OUT_PUT_CSV)




if __name__ == "__main__":
    cntlr = Cntlr()
    cntlr.run(const.XBRL_TEMP_PATH)