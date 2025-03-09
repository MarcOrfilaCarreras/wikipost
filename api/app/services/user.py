from datetime import datetime
from datetime import timedelta

from app.db.connector import DatabaseConnector
from app.db.models.article import Article
from app.db.models.post import Post
from app.db.models.user import Settings
from app.db.models.user import User
from app.extensions import logging
from app.utils.jwt import JWTManager


def create_user(*, email=None, password=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO users (email, password)
                              VALUES (?, ?)
                              RETURNING id, email, password, created_at""",
                           (email, password))

            if data := cursor.fetchone():
                user = User(id=data[0], email=data[1],
                            password=data[2], created_at=data[3])
                conn.commit()
                return user

            return None

    except Exception as e:
        logging.error(
            f'[DATABASE] Error creating user with email {email}: {e}')
        return None


def create_user_settings(*, user=None, ai_prompt=None, instagram_username=None, instagram_password=None, instagram_email=None, instagram_email_password=None, scheduler=None, scheduler_interval=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO users_settings (user, ai_prompt, instagram_username, instagram_password, instagram_email, instagram_email_password, scheduler, scheduler_interval)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                              RETURNING id, ai_prompt, instagram_username, instagram_password, instagram_email, instagram_email_password, scheduler, scheduler_interval, created_at""",
                           (user, ai_prompt, instagram_username, instagram_password, instagram_email, instagram_email_password, scheduler, scheduler_interval))

            if data := cursor.fetchone():
                settings = Settings(id=data[0], ai_prompt=data[1], instagram_username=data[2],
                                    instagram_password=data[3], instagram_email=data[4], instagram_email_password=data[5], scheduler=data[6], scheduler_interval=data[7], created_at=data[8])
                conn.commit()
                return settings

            return None

    except Exception as e:
        logging.error(
            f'[DATABASE] Error creating user settings {user}: {e}')
        return None


def get_user_settings(*, user=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""SELECT id, ai_prompt, instagram_username, instagram_password, instagram_email, instagram_email_password, scheduler, scheduler_interval, created_at
                              FROM users_settings WHERE user = ?""",
                           (user, ))

            if data := cursor.fetchone():
                settings = Settings(id=data[0], ai_prompt=data[1], instagram_username=data[2],
                                    instagram_password=data[3], instagram_email=data[4], instagram_email_password=data[5], scheduler=data[6], scheduler_interval=data[7], created_at=data[8])
                return settings

            return None

    except Exception as e:
        logging.error(
            f'[DATABASE] Error getting settings of the user {user}: {e}')
        return None


def update_user_settings(*, user=None, ai_prompt=None, instagram_username=None, instagram_password=None, instagram_email=None, instagram_email_password=None, scheduler=None, scheduler_interval=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""UPDATE users_settings SET ai_prompt = ?, instagram_username = ?, instagram_password = ?, instagram_email = ?, instagram_email_password = ?, scheduler = ?, scheduler_interval = ? WHERE user = ?
                              RETURNING id, ai_prompt, instagram_username, instagram_password, instagram_email, instagram_email_password, scheduler, scheduler_interval, created_at""",
                           (ai_prompt, instagram_username, instagram_password, instagram_email, instagram_email_password, scheduler, scheduler_interval, user))

            if data := cursor.fetchone():
                settings = Settings(id=data[0], ai_prompt=data[1], instagram_username=data[2],
                                    instagram_password=data[3], instagram_email=data[4], instagram_email_password=data[5], scheduler=data[6], scheduler_interval=data[7], created_at=data[8])
                conn.commit()
                return settings

            return None

    except Exception as e:
        logging.error(
            f'[DATABASE] Error creating user settings {user}: {e}')
        return None


def get_user_by_email(*, email=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""SELECT id, email, password, created_at
                              FROM users WHERE email = ?""",
                           (email, ))

            if data := cursor.fetchone():
                user = User(id=data[0], email=data[1],
                            password=data[2], created_at=data[3])
                return user

            return None

    except Exception as e:
        logging.error(f'[DATABASE] Error getting user with email {email}: {e}')
        return None


def get_user_jwt_token(*, user=None):
    return JWTManager.create({'id': user.id, 'exp': (datetime.utcnow() + timedelta(days=7)).timestamp()})


def get_user_articles(*, user=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""SELECT id, title, content, url, created_at
                              FROM articles WHERE user = ?""",
                           (user, ))

            articles = []
            for row in cursor.fetchall():
                articles.append(Article(id=row[0], title=row[1],
                                content=row[2], url=row[3], created_at=row[4]))

            return articles if articles else None

    except Exception as e:
        logging.error(
            f'[DATABASE] Error getting articles of the user {user}: {e}')
        return None


def get_user_posts(*, user=None, allowed=None, published=False):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            query = """SELECT id, content, url, allowed, published, created_at
                       FROM posts WHERE user = ?"""
            params = [user]

            if allowed is not None:
                query += ' AND allowed = ?'
                params.append(allowed)

            if published is not None:
                query += ' AND published = ?'
                params.append(published)

            cursor.execute(query, tuple(params))

            posts = [
                Post(id=row[0], content=row[1], url=row[2],
                     allowed=row[3], published=row[4], created_at=row[5])
                for row in cursor.fetchall()
            ]

            return posts if posts else None

    except Exception as e:
        logging.error(
            f'[DATABASE] Error getting posts of the user {user}: {e}')
        return None
