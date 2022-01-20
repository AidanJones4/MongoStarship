from starship_project import *


def get_all_jsons_test():

    assert get_all_jsons("https://swapi.dev/api/starships") == get_all_jsons("https://swapi.dev/api/starships")



