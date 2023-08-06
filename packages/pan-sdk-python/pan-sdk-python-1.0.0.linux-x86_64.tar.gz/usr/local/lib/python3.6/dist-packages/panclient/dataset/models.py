from panclient.common.abstract_model import AbstractModel


class CreateGetDataset(AbstractModel):
    def __init__(self):
        self.header = None
        self.id = None


class CreateDataset(AbstractModel):
    def __init__(self):
        self.displayType = None
        self.remark = None
        self.rolesId = None
        self.schemaIds = None
        self.title = None
        self.userIds = None
        self.header = None