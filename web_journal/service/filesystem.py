# AUTOGENERATED! DO NOT EDIT! File to edit: 40b_service_filesystem.ipynb (unless otherwise specified).

__all__ = ['posts_list_to_dict', 'migrate', 'ServiceFilesystem', 'before_request', 'after_request', 'init_service']

# Cell
import json,time,datetime,re
from pathlib import Path

# Cell
def posts_list_to_dict(posts,key='id'):
    "Convert a list of dictionaries to a dictionary of dictionaries"
    return {post[key]:post for post in posts}

# Cell
def migrate(data_dir,output_dir=None):
    posts_file_re=re.compile(r'posts-(?:\d{13}).json')
    data_dir=Path(data_dir)
    output_dir=data_dir if output_dir is None else Path(output_dir)
    for f_name in data_dir.iterdir():
        if not posts_file_re.fullmatch(f_name.name): continue
        with open(f_name) as f: posts = json.load(f)
        if not posts: continue
        print('migrating',f_name,'to',output_dir)
        if not 'status' in posts[0]:
            for post in posts:
                post['last_updated']=post['created']
                post['status']=50 if post['is_deleted']==0 else 20
                del post['is_deleted']
        # subsequent migrations might do something like
        # if not 'other_key' in posts[0]: ...
        with open(output_dir/f_name.name,'w') as f: json.dump(posts,f)

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
        user=self.read_user_by_id(post['author_id'])
        post['username']='Unknown user' if user is None else user['username']
        return post

    def _posts(self,author_id):
        if (self.data_dir/f'posts-{author_id}.json').is_file():
            with open(self.data_dir/f'posts-{author_id}.json') as f:
                return json.load(f)
        return []

    def read_posts_by_author_id(self,author_id):
        return [self._add_username(p) for p in self._posts(author_id) if p['status']>30]

    def read_post_by_id(self,author_id,id):
        for post in self._posts(author_id):
            if post['id']==id: return self._add_username(post)
        return None

    def _now(self):
        return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    def create_post(self,author_id,title,body):
        posts=self._posts(author_id)
        id,_now=round(time.time()*1000),self._now()
        posts.insert(0,dict(id=id,author_id=author_id,title=title,body=body,
                            created=_now,last_updated=_now,status=50))
        with open(self.data_dir/f'posts-{author_id}.json','w') as f: json.dump(posts,f)
        return id

    def update_post_by_id(self,author_id,id,keys,values):
        posts=self._posts(author_id)
        for post in posts:
            if post['id']==id:
                for key,value in zip(keys,values): post[key]=value
                post['last_updated']=self._now()
                with open(self.data_dir/f'posts-{author_id}.json','w') as f: json.dump(posts,f)
                return post
        return None

    def prepare_posts_file_by_author_id(self,author_id):
        if (self.data_dir/f'posts-{author_id}.json').is_file():
            return self.data_dir,f'posts-{author_id}.json'
        return None,None

    def upload_posts_from_file(self,author_id,file):
        # TODO: handle non-json formats
        with open(file) as f:
            posts=json.load(f)
            for post in posts: post['author_id']=author_id
            posts=posts_list_to_dict(posts)
        posts.update(posts_list_to_dict(self._posts(author_id)))
        posts=sorted(posts.values(), key=lambda post: post['id'], reverse=True)
        with open(self.data_dir/f'posts-{author_id}.json','w') as f: json.dump(posts,f)

# Cell
def before_request(app):
    return ServiceFilesystem(app.config['DATA_DIR'])

# Cell
def after_request(app,service):
    pass

# Cell
def init_service(app):
    print('service.filesystem.init_service')