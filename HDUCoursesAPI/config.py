import os


def mongo_url() -> str:
    url = os.environ['MONGODB_URL']

    if mongo_url == '':
        url = 'mongodb://localhost'
    return url
