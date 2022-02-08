import petl
import os


class ApiDataSaver:
    def save(self, api_data):
        pass


class CsvApiDataSaver(ApiDataSaver):
    def __init__(self, transformer, filepath):
        self.transformer = transformer
        self.filepath = filepath

    def save(self, people_api_data):
        people_data_table = petl.fromdicts(people_api_data)
        people_data_table = self.transformer.transform_people_table(people_data_table)

        if os.path.exists(self.filepath):
            petl.appendcsv(people_data_table, self.filepath)
        else:
            petl.tocsv(people_data_table, self.filepath)
