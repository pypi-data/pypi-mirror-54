from panclient.common.abstract_model import AbstractModel


class GraphProduct(AbstractModel):
    def __init__(self):
        self.workspaceId = None


class SemSetList(AbstractModel):
    def __init__(self):
        self.SemSetList = None


class SemSet(AbstractModel):
    def __init__(self):
        self.disabled = None
        self.id = None
        self.info = None
        self.label = None
        self.type = None
        self.credentials = None
        self.dataSetId = None
        self.entityClass = None
        self.wires = None
        self.x = None
        self.y = None
        self.z = None
        self.pickType = None
        self.opt = None
        self.value = None
        self.field = None
        self.analysis = None
        self.analysisId = None
        self.analysisType = None
        self.graphName = None
        self.oper = None