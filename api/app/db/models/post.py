class Post:
    def __init__(self, *, id=None, content=None, url=None, allowed=None, published=None, created_at=None, questions=None):
        self.id = id
        self.content = content
        self.url = url
        self.allowed = allowed
        self.published = published
        self.created_at = created_at
        self.questions = questions or []

    def get_questions(self):
        from app.services.post import get_questions_by_post

        self.questions = get_questions_by_post(id=self.id)
        return self.questions

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'url': self.url,
            'allowed': self.allowed,
            'published': self.published,
            'created_at': self.created_at,
            'questions': [q.to_dict() for q in self.get_questions()]
        }
