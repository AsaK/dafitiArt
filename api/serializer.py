from rest_framework import routers, serializers

from core.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'type', 'is_staff', 'created_at')