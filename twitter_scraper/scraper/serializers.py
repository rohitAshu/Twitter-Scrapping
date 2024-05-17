from rest_framework import serializers


class TwitterProfileSerializers(serializers.Serializer):
    Profile_name = serializers.CharField(required=True)
