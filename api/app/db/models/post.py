class Post:
    def __init__(self, *, id=None, content=None, url=None, allowed=None, published=None, created_at=None):
        self.id = id
        self.content = content
        self.url = url
        self.allowed = allowed
        self.published = published
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'url': self.url,
            'allowed': self.allowed,
            'published': self.published,
            'created_at': self.created_at
        }
