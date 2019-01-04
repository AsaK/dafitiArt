from django.contrib import admin

# Register your models here.
from art.models import ArtRequest, ArtRequestFile

admin.site.register(ArtRequest)
admin.site.register(ArtRequestFile)