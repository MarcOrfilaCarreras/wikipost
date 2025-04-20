class PostQuestion:
    def __init__(self, *, id=None, post=None, content=None, created_at=None, options=None):
        self.id = id
        self.post = post
        self.content = content
        self.created_at = created_at
        self.options = options or []

    def to_dict(self):
        return {
            'id': self.id,
            'post': self.post,
            'content': self.content,
            'created_at': self.created_at,
            'options': [opt.to_dict() for opt in self.options]
        }
