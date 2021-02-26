# AUTOGENERATED! DO NOT EDIT! File to edit: 40a_service_db.ipynb (unless otherwise specified).

__all__ = ['SCHEMA_SQL', 'ServiceDb', 'before_request', 'after_request', 'init_service']

# Cell
import sqlite3
from pathlib import Path

# Cell
SCHEMA_SQL="""
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  is_deleted INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
"""

# Cell
class ServiceDb:

    def __init__(self,database_file):
        self.db = sqlite3.connect(
            database_file, detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.db.row_factory = sqlite3.Row

    def read_user_by_id(self,id):
        return self.db.execute(
            "SELECT * FROM user WHERE id = ?", (id,)
        ).fetchone()

    def read_user_by_username(self,username):
        return self.db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

    def create_user(self,username,password):
        cursor=self.db.cursor()
        cursor.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, password),
        )
        self.db.commit()
        return cursor.lastrowid

    def read_posts_by_author_id(self,author_id):
        return self.db.execute(
            "SELECT p.id, title, body, strftime('%Y-%m-%d %H:%M:%S',created) created, author_id, username, is_deleted"
            "  FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE u.id = ?"
            "   AND p.is_deleted = 0"
            " ORDER BY created DESC",
            (author_id,)
        ).fetchall()

    def read_post_by_id(self,author_id,id):
        return self.db.execute(
            "SELECT p.id, title, body, strftime('%Y-%m-%d %H:%M:%S',created) created, author_id, username, is_deleted"
            "  FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.author_id = ?"
            "   AND p.id = ?",
            (author_id,id,),
        ).fetchone()

    def create_post(self,author_id,title,body):
        cursor=self.db.cursor()
        cursor.execute(
            "INSERT INTO post (author_id, title, body) VALUES (?, ?, ?)",
            (author_id, title, body),
        )
        self.db.commit()
        return cursor.lastrowid

    def update_post_by_id(self,author_id,id,title,body):
        # TODO: use author_id
        self.db.execute(
            "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
        )
        self.db.commit()

    def delete_post_by_id(self,author_id,id):
        # TODO: use author_id
        self.db.execute("UPDATE post SET is_deleted = 1 WHERE id = ?", (id,))
        self.db.commit()

# Cell
def before_request(app):
    return ServiceDb(Path(app.config['DATA_DIR'])/'web_journal.sqlite')

# Cell
def after_request(app,service):
    service.db.close()

# Cell
def init_service(app):
    print('service.db.init_service')
    service=ServiceDb(Path(app.config['DATA_DIR'])/'web_journal.sqlite')
    try:
        # This will raise an error if the user table has not been created ...
        service.read_user_by_id(0)
    except:
        # ... so we know we need to create the schema
        service.db.executescript(SCHEMA_SQL)