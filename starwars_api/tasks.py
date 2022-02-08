from starwars_api.models import get_datasets_directory_path
from starwars_api.api_data_downloader import ApiDataDownloader
from starwars_api.serializers import DatasetMetadataSerializer
from celery import shared_task

@shared_task
def download_api_character_data(data, context):
    file_store_directory = get_datasets_directory_path()
    downloader = ApiDataDownloader(file_store_directory)
    filepath = downloader.download()
    data['filepath'] = filepath
    metadata_serializer = DatasetMetadataSerializer(data=data, context=context)
    metadata_serializer.is_valid(raise_exception=True)
    metadata_serializer.create(metadata_serializer.validated_data)

