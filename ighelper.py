import json
from typing import List, Set, Dict, Generator
from urllib.parse import urlencode

import requests

from settings import *


class IgHelper(object):
    def __init__(self):
        self.followers: List = list(self.extract_followers())
        self.following: List = list(self.extract_following())

    @property
    def followers_set(self) -> Set:
        return set(x['node']['username'] for x in self.followers)

    @property
    def following_set(self) -> Set:
        return set(x['node']['username'] for x in self.following)

    @property
    def unfollowers(self) -> Set:
        return self.following_set - self.followers_set

    @property
    def unfollowing(self) -> Set:
        return self.followers_set - self.following_set

    def dump_to_mongo(self):
        """
        Dumps followers and following to MongoDB
        :return: 
        """
        from pymongo import MongoClient
        client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        db = client[MONGO_DB]
        followers_col = db[f'{TARGET_ID}_followers']
        following_col = db[f'{TARGET_ID}_following']
        followers_col.insert_many(self.followers)
        following_col.insert_many(self.following)

    @staticmethod
    def _extract_entities(query_hash: str, entity_id: str) -> Generator[Dict]:
        """
        Generator that yields the corresponding entities based on the parameters.
        :param query_hash: The Query hash used to Request the entity type
        :param entity_id: string that defines the key inside the response to access the entity
        """
        query = {
            "query_hash": query_hash,
            "variables": json.dumps({
                "id": TARGET_ID,
                "include_reel": True,
                "first": 500
            })
        }

        has_next_page = True
        while has_next_page:
            querystring = urlencode(query)
            resp = requests.request("GET", BASE_URL, params=querystring, headers=HEADERS)
            data = json.loads(resp.content)
            page_info = data['data']['user'][entity_id]['page_info']
            edges = data['data']['user'][entity_id]['edges']
            has_next_page = page_info['has_next_page']

            for edge in edges:
                edge["_id"] = edge['node']['id']
                print(f'{entity_id} - yielding entity: {edge}')
                yield edge

            if has_next_page:
                query['variables'] = json.dumps({
                    "id": TARGET_ID,
                    "include_reel": True,
                    "first": 500,
                    "after": page_info['end_cursor']
                })

    @staticmethod
    def extract_following() -> Generator[Dict]:
        """
        Runs extraction of following doing paginated requests
        :return: list of nodes (dicts) containing the following accounts
        """
        yield from IgHelper._extract_entities(query_hash=FOLLOWING_QUERY_HASH, entity_id='edge_follow')

    @staticmethod
    def extract_followers() -> Generator[Dict]:
        """
        Runs extraction of followers doing paginated requests
        :return: list of nodes (dicts) containing the followers
        """
        yield from IgHelper._extract_entities(query_hash=FOLLOWERS_QUERY_HASH, entity_id='edge_followed_by')
