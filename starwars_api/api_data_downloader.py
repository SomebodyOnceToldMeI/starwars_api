import requests
import json


class ApiDataDownloader:
    api_url = 'https://swapi.dev/api/'
    homeworlds = {}

    def __init__(self, data_saver):
        self.data_saver = data_saver

    def download(self):
        next_page = None
        while True:
            data = self._get_people_data(next_page_url=next_page)
            next_page = data['next']
            people_data = data['results']
            self._fill_homeworlds(people_data)
            self.data_saver.save(people_data)
            if not next_page:
                break

    def _get_people_data(self, next_page_url=None):
        if not next_page_url:
            url = self.api_url + 'people/'
        else:
            url = next_page_url

        response = requests.get(url)
        data = json.loads(response.text)

        return data

    def _fill_homeworlds(self, people_data):
        for person in people_data:
            homeworld_url = person['homeworld']
            homeworld = self.homeworlds.get(homeworld_url)
            if not homeworld:
                homeworld = self._get_homeworld(homeworld_url)
                self.homeworlds[homeworld_url] = homeworld
            person['homeworld'] = homeworld

    def _get_homeworld(self, homeworld_url):
        response = requests.get(homeworld_url)
        data = json.loads(response.text)
        homeworld_name = data['name']
        return homeworld_name



