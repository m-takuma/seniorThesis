from enum import Enum
from arelle.ModelXbrl import ModelXbrl
from arelle.Cntlr import Cntlr
from arelle.ModelManager import ModelManager
from arelle.ModelInstanceObject import ModelFact
from arelle.ModelDtsObject import ModelConcept
from arelle.ModelInstanceObject import ModelContext
from datetime import timedelta
import const as const
import csv
from arelle.ModelRelationshipSet import ModelRelationshipSet
class ViewFacts():
    class Column(Enum):
        Label = "Label"
        Name = "Name"
        LocalName = "LocalName"
        Namespace = "Namespace"
        contextRef = "contextRef"
        unitRef = "unitRef"
        Dec = "Dec"
        Prec = "Prec"
        Lang = "Lang"
        Value = "Value"
        EntityScheme = "EntityScheme"
        EntityIdentifier = "EntityIdentifier"
        Period = "Period"
        Dimensions = "Dimensions"           
        
        @property
        def label(self):
            if self == ViewFacts.Column.Label:
                return "要素名"
            elif self == ViewFacts.Column.Name:
                return "Name"
            elif self == self.LocalName:
                return "LocalName"
            elif self == self.Namespace:
                return "Namespace"
            elif self == self.contextRef:
                return "contextRef"
            elif self == self.unitRef:
                return "unitRef"
            elif self == self.Dec:
                return "Dec"
            elif self == self.Prec:
                return "Prec"
            elif self == self.Lang:
                return "Lang"
            elif self == self.Value:
                return "Value"
            elif self == self.EntityScheme:
                return "EntityScheme"
            elif self == self.EntityIdentifier:
                return "EntityIdentifier"
            elif self == self.Period:
                return "(開始日):(終了日/時点)"
            elif self == self.Dimensions:
                return "Dimensions"
            else:
                raise SystemError("don't dimension Column")

    def __init__(self, model_xbrl, outfile = const.OUT_PUT_CSV, cols: list[Column] = None):
        self.cols = cols
        self.modelXbrl: ModelXbrl = model_xbrl
        self.csv_file = open(outfile, "w", newline="", encoding='utf-8-sig')
        self.csv_writer = csv.writer(self.csv_file)

    def view(self):
        if self.cols:
            if not isinstance(self.cols, (list, self.Column)):
                raise SystemError()
        else:
            self.cols = [
                self.Column.Label,
                self.Column.contextRef,
                self.Column.Period,
                self.Column.Value
            ]
        if self.cols[0] not in [self.Column.Label, 
                                self.Column.Name, 
                                self.Column.LocalName]:
            raise SystemError()
        self.isCol0Label = self.cols[0] == self.Column.Label
        header = list(map(lambda col: col.label, self.cols))
        self.addRow(header)
        self.viewFacts(self.modelXbrl.facts)

    def addRow(self, cols):
        self.csv_writer.writerow(cols)


    def viewFacts(self, modelFacts: list[ModelFact]):
        for model_fact in modelFacts:
            concept: ModelConcept = model_fact.concept
            cols = []
            if concept is not None:
                if model_fact.isItem:
                    for col in self.cols:
                        if col == self.Column.Label:
                            cols.append( concept.label() )
                        elif col == self.Column.Name:
                            cols.append( model_fact.qname )
                        elif col == self.Column.LocalName:
                            cols.append( model_fact.qname.localName )
                        elif col == self.Column.Namespace:
                            cols.append( model_fact.qname.namespaceURI )
                        elif col == self.Column.contextRef:
                            cols.append( model_fact.contextID )
                        elif col == self.Column.unitRef:
                            cols.append( model_fact.unitID )
                        elif col == self.Column.Dec:
                            cols.append( model_fact.decimals )
                        elif col == self.Column.Prec:
                            cols.append( model_fact.precision )
                        elif col == self.Column.Lang:
                            cols.append( "lang" )
                        elif col == self.Column.Value:
                            cols.append( "nil" if model_fact.xsiNil == "true" else "str len over" if len(model_fact.effectiveValue.strip()) > 30000 else model_fact.effectiveValue.strip() )
                            # TODO: 文字数が多いとExcelの表示が崩れるため対処
                        elif col == self.Column.EntityScheme:
                            cols.append( model_fact.context.entityIdentifier[0] )
                        elif col == self.Column.EntityIdentifier:
                            cols.append( model_fact.context.entityIdentifier[1] )
                        elif col == self.Column.Period:
                            context: ModelContext = model_fact.context
                            start_datetime = context.startDatetime.date() if context.startDatetime else "nil"
                            end_datetime = (context.endDatetime - timedelta(1)).date() if context.endDatetime else "nil"
                            cols.append( f"{start_datetime}:{end_datetime}")
            self.addRow(cols)

class ViewTable():
    def __init__(self, model_xbrl, outfile = const.OUT_PUT_CSV) -> None:
        self.model_xbrl: ModelXbrl = model_xbrl
        self.csv_file = open(outfile, "w", newline="", encoding="utf-8-sig")
        self.csv_writer = csv.writer(self.csv_file)
        self.relationship: ModelRelationshipSet = self.model_xbrl.relationshipSet("http://www.xbrl.org/2003/arcrole/parent-child")
    
    def view(self):
        uris = list(self.relationship.linkRoleUris)
        uris = list(map(lambda x: (self.model_xbrl.roleTypeDefinition(x), x), uris))
        uris.sort()

        for _, uri in uris:
            self.relationship: ModelRelationshipSet = self.model_xbrl.relationshipSet("http://www.xbrl.org/2003/arcrole/parent-child", linkrole=uri)
            for root_concept in self.relationship.rootConcepts:
                root_concept: ModelConcept
                self.add_row([root_concept.qname, root_concept.label()])
                self.follow_link(root_concept, 1)
        for i, model_obj in enumerate(model_xbrl.modelObjects):
            self.follow_link(model_obj, 1)
    
    def follow_link(self ,model_obj, indent=0):
        for parent_rel_model in self.relationship.fromModelObject(model_obj):
            parent_rel_model : ModelRelationshipSet
            to_model_obj: ModelConcept = parent_rel_model.toModelObject
            #parent_rel_model.fromModelObject.qname,parent_rel_model.fromModelObject.label(),
            self.model_xbrl.contexts
            self.add_row([to_model_obj.qname, to_model_obj.label()], indent)
            self.follow_link(to_model_obj, indent+1)
        
    def add_row(self, cols: list, indent: int = 0):
        import_cols = ([""]*indent) + cols
        self.csv_writer.writerow(import_cols)


if __name__ == "__main__":
    cntlr = Cntlr()
    modelmanager = ModelManager(cntlr)
    model_xbrl =  modelmanager.load(const.XBRL_TEMP_PATH)
    ViewTable(model_xbrl).view()
    '''
    relationships = model_xbrl.relationshipSet("XBRL-footnotes")
    for rel in relationships.modelRelationships:
        fact = rel.fromModelObject
        footnote = rel.toModelObject
        if fact is not None and footnote is not None:
            print("Fact: ", fact.xValue if fact.isNumeric else fact.stringValue)
            print("Footnote: ", footnote.text if hasattr(footnote, 'text') else None)
    '''