## Include Pycharm Source Folders as Modules
This is a very simple tool which just adds all source folders from a pycharm project to the
 search path. It is very useful when working with notebooks while all the clutter gets
  nicely organized in python modules via pycharm. 

If you have a pycharm project like
```
super-project
  fancy_calculations
    fancy_module
      __init__.py
  notebooks
    a notebook.ipynb
```
 
A notebooks first cell may look like:
```python
%matplotlib inline
%load_ext autoreload
%autoreload 2
from include_pycharm_modules import import_source_folders
import_source_folders("..")

import fancy_module 
```

