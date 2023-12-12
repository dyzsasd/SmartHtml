from typing import List

from smart_html.utils.mixin import JsonMixin


class Comment(JsonMixin):
    def __init__(self, text):
        self.text = text


class GlobalComment(Comment):
    def __init__(self, text):
        super.__init__(text)


class ElementComment(Comment):
    def __init__(self, _id, text):
        super.__init__(text)
        self._id = _id


class WebPageComment(JsonMixin):
    def __init__(self, global_comment: GlobalComment, element_comments: List[ElementComment]):
        self.global_comment = global_comment
        self.element_comments = element_comments
