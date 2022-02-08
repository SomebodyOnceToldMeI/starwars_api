from rest_framework import viewsets
from starwars_api.models import DatasetMetadata
from starwars_api.serializers import DatasetMetadataSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.paginator import Paginator
from starwars_api.tasks import download_api_character_data
from rest_framework.reverse import reverse
import petl


class DatasetMetadataViewSet(viewsets.ModelViewSet):
    queryset = DatasetMetadata.objects.all()
    serializer_class = DatasetMetadataSerializer

    def create(self, request):
        dataset_url_pattern = reverse('dataset-detail', request=request, args=['format'])
        data = request.data
        context = {'dataset_url_pattern': dataset_url_pattern}
        download_api_character_data.delay(data, context)
        return Response(data={'status': 'Dataset is being downloaded.'})


class DatasetViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        table = self.get_dataset_table(request, pk)
        if not table:
            return Response(data={'status': 'dataset does not exist.'})
        dicts = petl.dicts(table)
        paginator = Paginator(dicts, per_page=10)
        page_number = int(request.GET.get('page', 1))
        page = paginator.get_page(page_number)
        if page.has_previous():
            prev_page = request.build_absolute_uri('?page={}'.format(page_number - 1))
        else:
            prev_page = None

        if page.has_next():
            next_page = request.build_absolute_uri('?page={}'.format(page_number + 1))
        else:
            next_page = None

        dicts = list(page)

        response_dict = {'prev': prev_page, 'next': next_page, 'results': dicts}
        return Response(data=response_dict)

    @action(detail=True, methods=['post'])
    def value_count(self, request, pk):
        table = self.get_dataset_table(request, pk)
        if not table:
            return Response(data={'status': 'dataset does not exist.'})
        columns = request.data.get('columns')
        try:
            aggregated = petl.aggregate(table, key=columns, aggregation=len)
        except petl.errors.FieldSelectionError:
            return Response(data={'status': 'some of the provided columns does not exist.'})
        dicts = list(aggregated.dicts())
        return Response(data=dicts)

    def get_dataset_table(self, request, pk):
        metadata = DatasetMetadata.objects.filter(id=pk).first()
        if not metadata:
            return None
        filepath = metadata.filepath
        table = petl.fromcsv(filepath)

        return table

