def get_sql():
    return '''
    CREATE TABLE
    IF NOT EXISTS articles (
        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
        user INTEGER NOT NULL,
        title TEXT,
        content TEXT,
        url TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user) REFERENCES users (id)
    );
    '''
