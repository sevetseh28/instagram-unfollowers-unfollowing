# Put your Instagram account ID here (as a string)
TARGET_ID = ''

# Paste your instagram.com cookie here after logging in (see README.md)
COOKIE = ''
HEADERS = {
    'accept': "*/*",
    'dnt': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-US,en;q=0.9,es-UY;q=0.8,es;q=0.7",
    'cookie': COOKIE,
    'cache-control': "no-cache",
}

BASE_URL = 'https://www.instagram.com/graphql/query/'

FOLLOWING_QUERY_HASH = 'c56ee0ae1f89cdbd1c89e2bc6b8f3d18'
FOLLOWERS_QUERY_HASH = '7dd9a7e2160524fd85f50317462cff9f'

USE_MONGO = False
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'instagram'
