import yaml 
from pyhere import here

__config = None

def config():
    global __config
    if not __config:
        with open(here('movie_crawler','config.yaml'), mode='r') as f:
            __config = yaml.load(f, Loader=yaml.BaseLoader)

    return __config