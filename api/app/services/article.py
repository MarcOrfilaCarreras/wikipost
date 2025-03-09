from app.db.connector import DatabaseConnector
from app.db.models.article import Article
from app.extensions import logging


def create_article(*, user=None, title=None, content=None, url=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO articles (user, title, content, url)
                              VALUES (?, ?, ?, ?)
                              RETURNING id, title, content, url, created_at""",
                           (user, title, content, url,))

            if data := cursor.fetchone():
                article = Article(id=data[0], title=data[1],
                                  content=data[2], url=data[3], created_at=data[4])
                conn.commit()
                return article

            return None

    except Exception as e:
        logging.error(
            f'[DATABASE] Error creating article: {e}')
        return None


def get_article(*, id=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""SELECT id, title, content, url, created_at from articles where id = ?""",
                           (id, ))

            if data := cursor.fetchone():
                article = Article(id=data[0], title=data[1],
                                  content=data[2], url=data[3], created_at=data[4])

                return article

            return None

    except Exception as e:
        logging.error(
            f'[DATABASE] Error getting article: {e}')
        return None


def delete_article(*, id=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""DELETE FROM articles WHERE id = ?""", (id,))
            conn.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False

    except Exception as e:
        logging.error(
            f'[DATABASE] Error deleting article: {e}')
        return False
