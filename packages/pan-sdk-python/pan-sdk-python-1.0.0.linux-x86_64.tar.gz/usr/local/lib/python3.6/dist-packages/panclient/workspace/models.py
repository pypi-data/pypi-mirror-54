from panclient.common.abstract_model import AbstractModel


class ProductRequest(AbstractModel):
    def __init__(self):
        self.kind = None
        self.productId = None
        self.title = None
        self.includeExtended = None
        self.params = None
        self.preview = None
        self.vertexIds = None


class NewProductRequest(AbstractModel):
    def __init__(self):
        self.data = None
        self.projectId = None
        self.title = None
        self.type = None


class Vertices:
    def __init__(self):
        self.isVirtual = None
        self.vertexId = None
        self.x = None
        self.y = None
        self.conceptTypes = None


class GraphVertices(AbstractModel):
    def __init__(self):
        self.analysisId = None
        self.vertices = None


class MultipleVertices(AbstractModel):
    def __init__(self):
        self.workspaceId = None
        self.vertexIds = None
        self.includeAncillary = None


class FindRelateRequest(AbstractModel):
    def __init__(self):
        self.graphVertexIds = None
        self.limitEdgeLabel = None
        self.limitParentConceptId = None


# search condition
class SearchRequest(AbstractModel):
    def __init__(self):
        self.fromBrocade = None
        self.searchItems = None


class SearchItem(AbstractModel):
    def __init__(self):
        self.conceptTypes = None
        self.filters = None
        self.keyword = None
        self.start = None
        self.type = None


class Filter(AbstractModel):
    def __init__(self):
        self.predicate = None
        self.propertyId = None
        self.value = None
