# We Journal
> A place to plan and journal inspired by coursera learning how to learn.


## Install

`pip install ` TODO:

# Developers

```
git config --global core.autocrlf input
```

```
conda create -n web_journal python==3.8 -y
conda activate web_journal
pip install fastscript==1.0.0 fastcore==1.3.10 nbdev==1.1.5 jupyter
cd github *** nav to where you want this project to live on your filesystem
git clone https://github.com/pete88b/web_journal.git
nbdev_install_git_hooks
jupyter notebook
```

## Type checking with mypy

```
!pip install mypy
```

Then from the storage_tools project folder
```
nbdev_build_lib
mypy web_journal/core.py
```

For now, I'm ignoring the "Skipping analyzing 'azure': found module but no type hints or library stubs" error
