class PostQuestionOption:
    def __init__(self, *, id=None, question=None, content=None, is_correct=None, created_at=None):
        self.id = id
        self.question = question
        self.content = content
        self.is_correct = is_correct
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'content': self.content,
            'is_correct': self.is_correct,
            'created_at': self.created_at
        }
