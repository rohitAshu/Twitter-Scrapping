
from rest_framework import serializers
class TwiiterProfileSerializers(serializers.Serializer):

    Profile_name = serializers.CharField(required=True)