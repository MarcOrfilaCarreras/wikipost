def get_sql():
    return '''
    CREATE TABLE IF NOT EXISTS users_settings (
        id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
        user TEXT NOT NULL,
        ai_prompt TEXT,
        instagram_username TEXT DEFAULT "",
        instagram_password TEXT DEFAULT "",
        instagram_email TEXT DEFAULT "",
        instagram_email_password TEXT DEFAULT "",
        scheduler TEXT DEFAULT "",
        scheduler_interval TEXT DEFAULT "",
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user) REFERENCES users (id)
    );
    '''
