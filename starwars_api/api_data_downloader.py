import requests
import json
import os
import petl
import datetime


def transform_date(str_date):
    date = datetime.datetime.strptime(str_date, "%Y-%m-%dT%I-%M-%S.%f")
    new_format_date = date.strftime("%Y-%m-%d")
    return new_format_date


class ApiDataDownloader:
    api_url = 'https://swapi.dev/api/'
    homeworlds = {}

    def __init__(self, file_store_directory):
        self.filepath = self._get_filepath(file_store_directory)

    def _get_filepath(self, file_store_directory):
        existing_datasets = os.listdir(file_store_directory)
        existing_datasets = [dataset for dataset in existing_datasets if '.csv' in dataset]
        if existing_datasets:
            existing_datasets_without_extension = [os.path.splitext(dataset)[0] for dataset in existing_datasets]
            dataset_indexes = [int(dataset[-1]) for dataset in existing_datasets_without_extension]
            last_dataset_index = max(dataset_indexes)
        else:
            last_dataset_index = -1
        filepath = os.path.join(file_store_directory, 'dataset_{}.csv'.format(last_dataset_index+1))
        return filepath

    def download(self):
        next_page = None
        while True:
            data = self._get_people_data(next_page_url=next_page)
            next_page = data['next']
            people_data = data['results']
            self._fill_homeworlds(people_data)
            self._save(people_data)
            if not next_page:
                break

        return self.filepath

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

    def _save(self, people_data):
        people_data_table = petl.fromdicts(people_data)
        people_data_table = self._transform_people_table(people_data_table)

        if os.path.exists(self.filepath):
            petl.appendcsv(people_data_table, self.filepath)
        else:
            petl.tocsv(people_data_table, self.filepath)

    def _transform_people_table(self, people_data_table):
        dates_to_drop = ['created', ]
        references_to_drop = ['films', 'vehicles', 'starships', 'species']

        people_data_table = petl.rename(people_data_table, 'edited', 'date')
        people_data_table = petl.convert(people_data_table, 'date', transform_date)

        for date_field in dates_to_drop:
            people_data_table = petl.cutout(people_data_table, date_field)

        for reference_field in references_to_drop:
            people_data_table = petl.cutout(people_data_table, reference_field)

        return people_data_table
