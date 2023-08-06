from panclient.common.abstract_model import AbstractModel


class CreateSchema(AbstractModel):
    def __init__(self):
        return


    #def _deserialize(self, params):
        #self.username = params.get("username")
        #return


class CreateSchemaConcept(AbstractModel):
    def __init__(self):
        self.color = None
        self.displayName = None
        self.glyphIconHref = None
        self.id = None
        self.parentConcept = None
        self.title = None
        self.header = {}

    def _deserialize(self, params):
        self.color = params.get("color")
        self.displayName = params.get("displayName")
        self.glyphIconHref = params.get("glyphIconHref")
        self.id = params.get("id")
        self.parentConcept = params.get("parentConcept")
        self.title = params.get("title")


class CreateAutoMapping(AbstractModel):
    def __init__(self):
        self.id = None
        self.header = {}

    def _deserialize(self, params):
        self.id = params.get("id")


class CreateSystemSchema(AbstractModel):
    def __init__(self):
        self.dataJson = None
        self.dataSet = None

    def _deserialize(self, params):
        self.id = params.get("dataJson")
        self.dataSet = params.get("dataSet")