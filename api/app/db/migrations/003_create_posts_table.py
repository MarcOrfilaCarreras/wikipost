def get_sql():
    return '''
    CREATE TABLE
    IF NOT EXISTS posts (
        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
        user INTEGER NOT NULL,
        content TEXT,
        url TEXT,
        allowed BOOLEAN DEFAULT FALSE,
        published BOOLEAN DEFAULT FALSE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user) REFERENCES users (id)
    );
    '''
