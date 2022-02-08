import petl
import os


class ApiDataSaver:
    def save(self, api_data):
        pass


class CsvApiDataSaver(ApiDataSaver):
    def __init__(self, transformer, file_store_directory):
        self.transformer = transformer
        self.filepath = self._get_filepath(file_store_directory)

    def save(self, people_api_data):
        people_data_table = petl.fromdicts(people_api_data)
        people_data_table = self.transformer.transform_people_table(people_data_table)

        if os.path.exists(self.filepath):
            petl.appendcsv(people_data_table, self.filepath)
        else:
            petl.tocsv(people_data_table, self.filepath)

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
