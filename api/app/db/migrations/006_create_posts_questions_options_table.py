def get_sql():
    return '''
    CREATE TABLE
    IF NOT EXISTS posts_questions_options (
        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
        question TEXT NOT NULL,
        content TEXT NOT NULL,
        is_correct BOOLEAN DEFAULT FALSE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (question) REFERENCES posts_questions (id) ON DELETE CASCADE
    );
    '''
