from rest_framework import serializers
from starwars_api.models import DatasetMetadata


class DatasetMetadataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DatasetMetadata
        fields = ['filepath', 'date', 'dataset_url', ]

    def create(self, validated_data):
        metadata = DatasetMetadata.objects.create(filepath=validated_data['filepath'])
        metadata.dataset_url = self.context['dataset_url_pattern'].replace('format', str(metadata.id))
        metadata.save()
        return metadata
