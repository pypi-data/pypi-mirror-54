from panclient.common.abstract_model import AbstractModel


class CreateLoginRequest(AbstractModel):
    def __init__(self):
        self.username = None
        self.password = None

    def _deserialize(self, params):
        self.username = params.get("username")
        self.password = params.get("password")


class CreateLoginResponse(AbstractModel):
    def __init__(self):
        self.Status = None

    def _deserialize(self, params):
        self.Status = params.get("success")


