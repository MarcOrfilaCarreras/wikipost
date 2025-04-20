def get_sql():
    return '''
    CREATE TABLE
    IF NOT EXISTS posts_questions (
        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
        post TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post) REFERENCES posts (id) ON DELETE CASCADE
    );
    '''
