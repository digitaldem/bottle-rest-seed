# Standard Library imports
from glob import glob
from importlib import import_module
from os import path, sep

# Package imports

# Local imports


# Automagically import all python files as valid bottle hooks
map(import_module,
    {'.'.join(path.splitext(f)[0].split(sep))
        for f in glob(path.join(path.dirname(__file__), '*.py*'))
        if not path.basename(f).startswith('__init__')})

# Remove std imports so the namespace remains clean
del glob
del import_module
del path
del sep
