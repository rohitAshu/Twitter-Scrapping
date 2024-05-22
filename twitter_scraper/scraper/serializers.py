from rest_framework import serializers


class TwitterProfileSerializers(serializers.Serializer):
    Profile_name = serializers.CharField(required=True)


class TweetHashtagSerializer(serializers.Serializer):
    hashtags = serializers.CharField(required=True)


class TweetUrlSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)
    post_ids = serializers.ListField(child=serializers.IntegerField(), required=True)

    @staticmethod
    def validate_post_id(value):
        try:
            # Try to convert the value to an integer
            post_id_int = int(value)
        except ValueError:
            # If conversion fails, raise a validation error
            raise serializers.ValidationError("Post ID must be an integer")

        # Return the integer value
        return post_id_int