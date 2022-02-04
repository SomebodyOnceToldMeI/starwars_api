from django.shortcuts import render
from rest_framework import viewsets
from starwars_api.models import DatasetMetadata
from starwars_api.serializers import DatasetMetadataSerializer
from starwars_api.api_data_downloader import ApiDataDownloader
from starwars_api.models import get_datasets_directory_path



class DatasetMetadataViewSet(viewsets.ModelViewSet):
    queryset = DatasetMetadata.objects.all()
    serializer_class = DatasetMetadataSerializer

    def create(self, request):
        file_store_directory = get_datasets_directory_path()
        downloader = ApiDataDownloader(file_store_directory)
        filepath = downloader.download()
        request.data['filepath'] = filepath
        return super().create(request)

