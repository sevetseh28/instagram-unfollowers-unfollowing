import json
from typing import List, Set
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
    def extract_following() -> List[dict]:
        """
        Runs extraction of following doing paginated requests
        :return: list of nodes (dicts) containing the following accounts
        """
        query = {
            "query_hash": FOLLOWING_QUERY_HASH,
            "variables": json.dumps({
                "id": TARGET_ID,
                "include_reel": True,
                "first": 500
            })
        }

        # FOLLOWING
        querystring = urlencode(query)
        resp = requests.request("GET", BASE_URL, params=querystring, headers=HEADERS)
        data = json.loads(resp.content)
        page_info = data['data']['user']['edge_follow']['page_info']
        edges = data['data']['user']['edge_follow']['edges']

        while True:
            for edge in edges:
                edge["_id"] = edge['node']['id']
                print(f'FOLLOWING: {edge}')
                yield edge

            has_next_page = page_info['has_next_page']
            if has_next_page:
                new_query = {
                    "query_hash": FOLLOWING_QUERY_HASH,
                    "variables": json.dumps({
                        "id": TARGET_ID,
                        "include_reel": True,
                        "first": 500,
                        "after": page_info['end_cursor']
                    })
                }
                querystring = urlencode(new_query)
                resp = requests.request("GET", BASE_URL, params=querystring, headers=HEADERS)
                data = json.loads(resp.content)
                page_info = data['data']['user']['edge_follow']['page_info']
                edges = data['data']['user']['edge_follow']['edges']
            else:
                return

    @staticmethod
    def extract_followers() -> List[dict]:
        """
        Runs extraction of followers doing paginated requests
        :return: list of nodes (dicts) containing the followers
        """
        query = {
            "query_hash": FOLLOWERS_QUERY_HASH,
            "variables": json.dumps({
                "id": TARGET_ID,
                "include_reel": True,
                "first": 500
            })
        }

        # EXTRACT FOLLOWERS
        querystring = urlencode(query)
        resp = requests.request("GET", BASE_URL, params=querystring, headers=HEADERS)
        data = json.loads(resp.content)
        page_info = data['data']['user']['edge_followed_by']['page_info']
        edges = data['data']['user']['edge_followed_by']['edges']

        while True:
            for edge in edges:
                edge["_id"] = edge['node']['id']
                print(f'FOLLOWER: {edge}')
                yield edge

            has_next_page = page_info['has_next_page']
            if has_next_page:
                new_query = {
                    "query_hash": FOLLOWERS_QUERY_HASH,
                    "variables": json.dumps({
                        "id": TARGET_ID,
                        "include_reel": True,
                        "first": 500,
                        "after": page_info['end_cursor']
                    })
                }
                querystring = urlencode(new_query)
                resp = requests.request("GET", BASE_URL, params=querystring, headers=HEADERS)
                data = json.loads(resp.content)
                page_info = data['data']['user']['edge_followed_by']['page_info']
                edges = data['data']['user']['edge_followed_by']['edges']
            else:
                return
