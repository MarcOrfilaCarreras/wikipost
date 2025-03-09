class Article:
    def __init__(self, *, id=None, title=None, content=None, url=None, created_at=None):
        self.id = id
        self.title = title
        self.content = content
        self.url = url
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'created_at': self.created_at
        }
