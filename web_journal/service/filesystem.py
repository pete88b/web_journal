# AUTOGENERATED! DO NOT EDIT! File to edit: 40b_service_filesystem.ipynb (unless otherwise specified).

__all__ = ['ServiceFilesystem', 'before_request', 'after_request', 'init_service']

# Cell
import json,time,datetime
from pathlib import Path

# Cell
class ServiceFilesystem:
    # TODO: DRY
    def __init__(self,data_dir):
        self.data_dir=Path(data_dir)
        self.data_dir.mkdir(parents=True,exist_ok=True)

    def read_user_by_id(self,id):
        if (self.data_dir/'users.json').is_file():
            with open(self.data_dir/'users.json') as f:
                for user in json.load(f):
                    if user['id']==id: return user
        return None

    def read_user_by_username(self,username):
        if (self.data_dir/'users.json').is_file():
            with open(self.data_dir/'users.json') as f:
                for user in json.load(f):
                    if user['username']==username: return user
        return None

    def create_user(self,username,password):
        users=[]
        if (self.data_dir/'users.json').is_file():
            with open(self.data_dir/'users.json') as f: users=json.load(f)
        id=round(time.time()*1000)
        users.append(dict(id=id,username=username,password=password))
        with open(self.data_dir/'users.json','w') as f: json.dump(users,f)
        return id

    def _add_username(self,post):
        # TODO: check how slow this is ...
        post['username']=self.read_user_by_id(post['author_id'])['username']
        return post

    def read_posts_by_author_id(self,author_id):
        if (self.data_dir/f'posts-{author_id}.json').is_file():
            with open(self.data_dir/f'posts-{author_id}.json') as f:
                return [self._add_username(p) for p in json.load(f) if p['is_deleted']==0]
        return []

    def read_post_by_id(self,author_id,id):
        if (self.data_dir/f'posts-{author_id}.json').is_file():
            with open(self.data_dir/f'posts-{author_id}.json') as f:
                for post in json.load(f):
                    if post['id']==id: return self._add_username(post)
        return None

    def create_post(self,author_id,title,body):
        posts=[]
        if (self.data_dir/f'posts-{author_id}.json').is_file():
            with open(self.data_dir/f'posts-{author_id}.json') as f: posts=json.load(f)
        id=round(time.time()*1000)
        _now=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
#         _now=datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        posts.insert(0,dict(id=id,author_id=author_id,title=title,body=body,created=_now,is_deleted=0))
        with open(self.data_dir/f'posts-{author_id}.json','w') as f: json.dump(posts,f)
        return id

    def update_post_by_id(self,author_id,id,title,body):
        if (self.data_dir/f'posts-{author_id}.json').is_file():
            with open(self.data_dir/f'posts-{author_id}.json') as f:
                posts = json.load(f)
                for post in posts:
                    if post['id']==id:
                        post['title'],post['body']=title,body
                        with open(self.data_dir/f'posts-{author_id}.json','w') as f: json.dump(posts,f)
                        return post
        return None

    def delete_post_by_id(self,author_id,id):
        if (self.data_dir/f'posts-{author_id}.json').is_file():
            with open(self.data_dir/f'posts-{author_id}.json') as f:
                posts = json.load(f)
                for post in posts:
                    if post['id']==id:
                        post['is_deleted']=1
                        with open(self.data_dir/f'posts-{author_id}.json','w') as f: json.dump(posts,f)
                        return post
        return None

# Cell
def before_request(app):
    return ServiceFilesystem(app.config['DATA_DIR'])

# Cell
def after_request(app,service):
    pass

# Cell
def init_service(app):
    print('service.filesystem.init_service')