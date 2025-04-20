import random

from app.db.connector import DatabaseConnector
from app.db.models.post import Post
from app.db.models.post_question import PostQuestion
from app.db.models.post_question_option import PostQuestionOption
from app.extensions import encryption
from app.extensions import logging
from app.external.instagram import Instagram
from app.services.user import get_user_posts
from app.services.user import get_user_settings
from app.utils.files import download_image
from app.utils.instagram import generate_instagram_poll


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

            if (len(post.get_questions()) > 0) and (path is not None):
                generate_instagram_poll(question = post.questions[0].content, answers = [str(o.content) for o in post.questions[0].options], background = path, path = '/tmp/' + post.questions[0].id + '.png')

                client.upload_history(path='/tmp/' + post.questions[0].id + '.png')

            updated_post_data = post.to_dict()
            updated_post_data['published'] = True
            updated_post_data.pop('created_at', None)
            updated_post_data.pop('questions', None)

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

def create_question(*, post=None, content=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO posts_questions (post, content)
                              VALUES (?, ?)
                              RETURNING id, post, content, created_at""",
                           (post, content,))

            if data := cursor.fetchone():
                question = PostQuestion(
                    id=data[0],
                    post=data[1],
                    content=data[2],
                    created_at=data[3]
                )
                conn.commit()
                return question

            return None

    except Exception as e:
        logging.error(f'[DATABASE] Error creating question: {e}')
        return None

def create_option(*, question=None, content=None, is_correct=False):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO posts_questions_options (question, content, is_correct)
                              VALUES (?, ?, ?)
                              RETURNING id, question, content, is_correct, created_at""",
                           (question, content, is_correct))

            if data := cursor.fetchone():
                option = PostQuestionOption(
                    id=data[0],
                    question=data[1],
                    content=data[2],
                    is_correct=data[3],
                    created_at=data[4]
                )
                conn.commit()
                return option

            return None

    except Exception as e:
        logging.error(f'[DATABASE] Error creating option: {e}')
        return None

def get_questions_by_post(*, id=None):
    try:
        with DatabaseConnector.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""SELECT id, post, content, created_at
                              FROM posts_questions
                              WHERE post = ?""",
                           (id,))
            question_rows = cursor.fetchall()

            questions = []

            for row in question_rows:
                question_id = row[0]
                question = PostQuestion(
                    id=row[0],
                    post=row[1],
                    content=row[2],
                    created_at=row[3]
                )

                cursor.execute("""SELECT id, question, content, is_correct, created_at
                                  FROM posts_questions_options
                                  WHERE question = ?""",
                               (question_id,))
                option_rows = cursor.fetchall()

                options = [
                    PostQuestionOption(
                        id=opt[0],
                        question=opt[1],
                        content=opt[2],
                        is_correct=opt[3],
                        created_at=opt[4]
                    ) for opt in option_rows
                ]

                question.options = options
                questions.append(question)

            return questions

    except Exception as e:
        logging.error(f'[DATABASE] Error getting questions and options for post {id}: {e}')
        return []
