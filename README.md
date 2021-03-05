# Web Journal
> A place to plan and journal. Inspired by coursera learning how to learn.


## Overview

This project starts with the [Flask basic blog](https://flask.palletsprojects.com/en/1.1.x/tutorial/) and makes it work as a journal for me (o:

At some point, I'll turn this into or create a [solid web app](https://solidproject.org/) but for now ... I need to  learn a few things about python apps with RDBMS and Azure deployments.

# Developers

```
git config --global core.autocrlf input
```

```
conda create -n web_journal python==3.8 -y
conda activate web_journal
pip install fastscript==1.0.0 fastcore==1.3.10 nbdev==1.1.5 jupyter
pip install Flask Markdown
cd github *** nav to where you want this project to live on your filesystem
git clone https://github.com/pete88b/web_journal.git
nbdev_install_git_hooks
jupyter notebook
```

TODO: see settings.ini dev_requirements

## Running the app locally

```
SET FLASK_APP=web_journal.web.app
SET FLASK_ENV=development
flask run
```

## Type checking with mypy

```
!pip install mypy
```

Then from the web_journal project folder
```
nbdev_build_lib
mypy web_journal/core.py
```
