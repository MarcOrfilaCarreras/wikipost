class User:
    def __init__(self, *, id=None, email=None, password=None, created_at=None):
        self.id = id
        self.email = email
        self.password = password
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at
        }


class Settings:
    def __init__(self, *, id=None, ai_prompt=None, instagram_username=None, instagram_password=None, instagram_email=None, instagram_email_password=None, scheduler=None, scheduler_interval=None, created_at=None):
        self.id = id
        self.ai_prompt = ai_prompt
        self.instagram_username = instagram_username
        self.instagram_password = instagram_password
        self.instagram_email = instagram_email
        self.instagram_email_password = instagram_email_password
        self.scheduler = scheduler
        self.scheduler_interval = scheduler_interval
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'ai_prompt': self.ai_prompt,
            'instagram_username': self.instagram_username,
            'instagram_password': self.instagram_password,
            'instagram_email': self.instagram_email,
            'instagram_email_password': self.instagram_email_password,
            'scheduler_interval': self.scheduler_interval,
            'created_at': self.created_at
        }
