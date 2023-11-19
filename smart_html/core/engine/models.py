from enum import Enum


class Role(Enum):
    USER = 1
    ASSISTANT = 2


class Message(object):
    @classmethod
    def user_message(cls, content: str):
        return cls(Role.USER, content)
    
    @classmethod
    def assistant_message(cls, content: str):
        return cls(Role.ASSISTANT, content)

    def __init__(self, role: Role, content: str):
        self.role = role
        self.content = content

    def to_api_message(self):
        raise NotImplementedError("to_api_message not implemented")


class Result(object):
    def html(self):
        raise NotImplementedError("html not implemented")
    
    def css(self):
        raise NotImplementedError("css not implemented")
    
    def javascript(self):
        raise NotImplementedError("javascript not implemented")
    