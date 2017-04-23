from rest_framework import serializers
from backend.models import Backend, LANGUAGE_CHOICES, STYLE_CHOICES


class BackendSerializer(serializers.ModelSerializer):
    restid = serializers.ReadOnlyField()

    class Meta:
        model = Backend
        fields = ('restid', 'created', 'name', 'address', 'rating', 'distance')
