import bson.objectid

from starship_project import *


def test_get_all_jsons():
    assert get_all_jsons("https://swapi.dev/api/starships") == get_all_jsons("https://swapi.dev/api/starships")


def test_api_url_to_id():
    assert api_url_to_id("https://swapi.dev/api/people/1/") == bson.objectid.ObjectId("61e58b579a1312ef9cb43900")


def test_update_jsons():
    assert update_jsons([{"pilots": ["https://swapi.dev/api/people/6/",
                                     "https://swapi.dev/api/people/1/",
                                     "https://swapi.dev/api/people/15/"]}]) ==\
                        [{"pilots": [bson.objectid.ObjectId("61e58b5c7e72d9e251d8a126"),
                                     bson.objectid.ObjectId("61e58b579a1312ef9cb43900"),
                                     bson.objectid.ObjectId("61e58b4d5b439b07d043f994")]}]

