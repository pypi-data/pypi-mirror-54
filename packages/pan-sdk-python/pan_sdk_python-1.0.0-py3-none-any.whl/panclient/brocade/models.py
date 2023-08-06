import time
from panclient.common.abstract_model import AbstractModel


class Brocade(AbstractModel):
    def __init__(self):
        self.brocadeId = None
        self.createTime = int(time.time())
        self.deleted = None
        self.endpoint = None
        self.publicState = None
        self.remark = None
        self.title = None
        self.uuid = None
        self.verb = None
        self.version = None


class BrocadeContent(AbstractModel):
    def __init__(self):
        self.type = None
        self.content = None


class CreateBrocade(AbstractModel):
    def __init__(self):
        self.content = None
        self.type = None
        self.dataSets = None
        self.description = None
        self.params = None
        self.title = None
        self.type = None