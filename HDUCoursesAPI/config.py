import os


def mongo_url() -> str:
    if 'MONGODB_URL' in os.environ.keys():
        url = os.environ['MONGODB_URL']
    else:
        url = 'mongodb://localhost'
    return url
