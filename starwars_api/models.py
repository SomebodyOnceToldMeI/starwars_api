from django.db import models
import os
from django.conf import settings


def get_datasets_directory_path():
    return os.path.join(settings.BASE_DIR, 'datasets')


class DatasetMetadata(models.Model):
    filepath = models.FilePathField(path=get_datasets_directory_path())
    date = models.DateTimeField(auto_now=True)
    dataset_url = models.URLField(max_length=200, blank=True)
