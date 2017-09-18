from rest_framework import serializers


class SearchFormSerializer(serializers.Serializer):
    query = serializers.CharField()

