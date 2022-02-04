from rest_framework import serializers
from starwars_api.models import DatasetMetadata


class DatasetMetadataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DatasetMetadata
        fields = ['filepath', 'date', ]
