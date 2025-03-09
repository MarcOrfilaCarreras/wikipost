import random

from app.db.connector import DatabaseConnector
from app.db.models.post import Post
from app.extensions import encryption
from app.extensions import logging
from app.external.instagram import Instagram
from app.services.user import get_user_posts
from app.services.user import get_user_settings
from app.utils.files import download_image


def create_post(*, user=None, content=None, url=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO posts (user, content, url)
                              VALUES (?, ?, ?)
                              RETURNING id, content, url, allowed, published, created_at""",
                           (user, content, url,))

            if data := cursor.fetchone():
                post = Post(id=data[0], content=data[1], url=data[2],
                            allowed=data[3], published=data[3], created_at=data[4])
                conn.commit()
                return post

            return None

    except Exception as e:
        logging.error(
            f'[DATABASE] Error creating post: {e}')
        return None


def get_post(*, id=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""SELECT id, content, url, allowed, published, created_at
                              FROM posts WHERE id = ?""", (id,))

            if data := cursor.fetchone():
                post = Post(id=data[0], content=data[1], url=data[2],
                            allowed=data[3], published=data[4], created_at=data[5])
                return post

            return None

    except Exception as e:
        logging.error(f'[DATABASE] Error retrieving post with id {id}: {e}')
        return None


def update_post(*, id=None, content=None, url=None, allowed=None, published=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""UPDATE posts
                              SET content = ?, url = ?, allowed = ?, published = ?
                              WHERE id = ?
                              RETURNING id, content, url, allowed, published, created_at""",
                           (content, url, allowed, published, id))

            if data := cursor.fetchone():
                post = Post(id=data[0], content=data[1], url=data[2],
                            allowed=data[3], published=data[4], created_at=data[5])
                conn.commit()
                return post

            return None

    except Exception as e:
        logging.error(f'[DATABASE] Error updating post with id {id}: {e}')
        return None


def delete_post(*, id=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""DELETE FROM posts WHERE id = ?""", (id,))
            conn.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False

    except Exception as e:
        logging.error(
            f'[DATABASE] Error deleting post: {e}')
        return False


def upload_post(*, user=None):
    attempts = 0
    max_retries=3

    while attempts < max_retries:
        try:
            posts = get_user_posts(user=user, allowed=True)
            if (posts is None) or (len(posts) <= 0):
                raise Exception('Allowed posts not found')

            post = posts[random.randint(0, len(posts) - 1)]

            settings = get_user_settings(user=user)
            if settings is None:
                raise Exception('Settings not found')

            path = download_image(post.url)
            if path is None:
                raise Exception("Image could't be downloaded")

            client = Instagram(username=settings.instagram_username,
                            password=encryption.decrypt(settings.instagram_password), email_address=settings.instagram_email, email_password=encryption.decrypt(settings.instagram_email_password))
            client.login()

            instagram_post_id = client.upload_photo(
                path=path, description=post.content)
            if (instagram_post_id == '') or (instagram_post_id == None):
                raise Exception('Instagram post could not be created')

            updated_post_data = post.to_dict()
            updated_post_data['published'] = True
            updated_post_data.pop('created_at', None)

            updated_post = update_post(**updated_post_data)
            if updated_post is None:
                raise Exception('Post could not be updated')

            return True

        except Exception as e:
            attempts += 1

            logging.error(f'[INSTAGRAM] Attempt {attempts} failed: {e}')

            if attempts >= max_retries:
                logging.error('[INSTAGRAM] Max retries reached. Upload failed.')
                return None
