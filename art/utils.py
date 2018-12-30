import os

from django.utils.timezone import now


def get_files_path(instance, filename):
    return os.path.join('art/files/', now().date().strftime("%Y/%m/%d"), filename)
