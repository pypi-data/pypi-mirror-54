from panclient.common.abstract_model import AbstractModel


class CreateUserRequest(AbstractModel):
    def __init__(self):
        self.userId = None
        self.username = None
        self.password = None
        self.displayname = None
        self.emailAddress = None
        self.roles = None
        self.status = None

    def _deserialize(self, params):
        self.userId = params.get("userId")
        self.username = params.get("username")
        self.password = params.get("password")
        self.displayname = params.get("displayname")
        self.emailAddress = params.get("emailAddress")
        self.roles = params.get("roles")
        self.status = params.get("status")
