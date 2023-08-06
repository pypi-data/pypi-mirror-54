from panclient.common.abstract_model import AbstractModel


class DatabaseRequest(AbstractModel):
    def __init__(self):
        self.adapter = None
        self.dbInstanceName = None
        self.dbName = None
        self.dbPassword = None
        self.dbRemark = None
        self.dbUser = None
        self.error = None
        self.host = None
        self.id = None
        self.port = None
        self.secondary = None
        self.show = None
        self.csvRemote = None


class JobRequest(AbstractModel):
    def __init__(self):
        self.datasetId = None
        self.loadOption = None
        self.selectedMappingIds = None
        self.cron = None


class LoadOption:
    OVERWRITE = "overwrite"
    UPDATE = "update"
    DUPLICATE = "duplicate"
    CRON = "cron"


class RdfFile(AbstractModel):
    def __init__(self):
        self.filePath = None
        self.dataSet = None
        self.mapping = None


class RdfMapping(AbstractModel):
    def __init__(self):
        self.dataSet = None


class JmsSchema(AbstractModel):
    def __init__(self):
        self.displayName = None
        self.schemaId = None


class JmsRequest(AbstractModel):
    def __init__(self):
        self.dataset = None
        self.datasetSchema = None
        self.id = None
        self.jmsConsumer = None
        self.jmsDrive = None
        self.jmsName = None
        self.jmsPassword = None
        self.jmsQueue = None
        self.jmsRemark = None
        self.jmsUrl = None
        self.jmsUser = None
        self.jsonHelpMess = None
        self.schemaList = None


class CsvRequest(AbstractModel):
    def __init__(self):
        self.filename = None
        self.filepath = None


class CsvPredicate(AbstractModel):
    def __init__(self):
        self.col = None
        self.predicateName = None
        self.type = None
        self.dateTimeFormat = None
        self.title = None
        self.index = None


class CsvEdge(AbstractModel):
    def __init__(self):
        self.startCsv = None
        self.startCsvCol = None
        self.startMapping = None
        self.endCsv = None
        self.endCsvCol = None
        self.endMapping = None


class CsvConfig(AbstractModel):
    def __init__(self):
        self.id = None
        self.fileName = None
        self.fileType = None
        self.conceptType = None
        self.header = None
        self.predicate = None
        self.titleRule = None
        self.edge = None
        self.edgeName = None


class CsvJob(AbstractModel):
    def __init__(self):
        self.config = None
        self.dataSet = None
        self.files = None