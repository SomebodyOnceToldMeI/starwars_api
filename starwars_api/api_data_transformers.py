import petl
import datetime


class ApiDataTransformer:
    def transform_people_table(self, people_data_table):
        pass


class NoReferenceApiDataTransformer(ApiDataTransformer):
    """Removes fields referencing another resources,
       transforms edited field to date and converts it to %Y-%m-%d format."""
    def transform_people_table(self, people_data_table):
        dates_to_drop = ['created', ]
        references_to_drop = ['films', 'vehicles', 'starships', 'species', 'url']

        people_data_table = petl.rename(people_data_table, 'edited', 'date')

        people_data_table = petl.convert(people_data_table, 'date', NoReferenceApiDataTransformer._transform_date)

        for date_field in dates_to_drop:
            people_data_table = petl.cutout(people_data_table, date_field)

        for reference_field in references_to_drop:
            people_data_table = petl.cutout(people_data_table, reference_field)

        return people_data_table

    @staticmethod
    def _transform_date(str_date):
        date = datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        new_format_date = date.strftime("%Y-%m-%d")
        return new_format_date
