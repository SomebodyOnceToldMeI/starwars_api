from rest_framework import serializers
from rest_framework.reverse import reverse
from starwars_api.models import DatasetMetadata


class DatasetMetadataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DatasetMetadata
        fields = ['filepath', 'date', 'dataset_url', ]

    def create(self, validated_data):
        metadata = DatasetMetadata.objects.create(filepath=validated_data['filepath'])
        metadata.dataset_url = reverse('dataset-detail', request=self.context['request'], args=[str(metadata.id)])
        metadata.save()
        return metadata