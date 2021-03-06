# AUTOGENERATED! DO NOT EDIT! File to edit: 50_web_app.ipynb (unless otherwise specified).

__all__ = ['create_app']

# Cell
import os
from flask import Flask, g
from pathlib import Path

# Cell
def create_app(test_config=None):
    "Create and configure an instance of the Flask application."
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        DATA_DIR=app.instance_path, # used by filesystem and DB service
#         USERNAME_SUFFIX='whatever' # Don't set username suffix by default
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)

    @app.route("/hello")
    def hello(): return "Hello, World!"

    # TODO: make the service module inport configurable
    import web_journal.service.filesystem as service_module
#     import web_journal.service.db as service_module

    service_module.init_service(app)

    @app.before_request
    def before_request():
        g.service=service_module.before_request(app)

    @app.after_request
    def after_request(response):
        service_module.after_request(app,g.service)
        return response

    from . import auth, blog
    # apply the blueprints to the app
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app